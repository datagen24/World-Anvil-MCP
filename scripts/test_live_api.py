#!/usr/bin/env python3
"""Live API Testing Script for World Anvil MCP Server.

This script performs live validation of World Anvil API write operations:
- World creation (if supported)
- Article creation (PUT)
- Article updates (PATCH)
- Article deletion (DELETE)
- Error handling validation

Usage:
    python scripts/test_live_api.py

Requirements:
    - WORLD_ANVIL_APP_KEY environment variable
    - WORLD_ANVIL_USER_TOKEN environment variable
    - Existing world ID for testing (creates test articles within it)

Safety:
    - Uses clearly named test articles (prefix: "MCP-TEST-")
    - Cleans up created resources after tests
    - Handles errors gracefully without affecting real data
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from world_anvil_mcp.client import WorldAnvilClient
from world_anvil_mcp.exceptions import (
    WorldAnvilAPIError,
    WorldAnvilAuthError,
    WorldAnvilNotFoundError,
    WorldAnvilRateLimitError,
)


class LiveAPITester:
    """Live API test orchestrator."""

    def __init__(self, world_id: str):
        """Initialize tester with target world.

        Args:
            world_id: World ID to use for article testing
        """
        self.world_id = world_id
        self.app_key = os.getenv("WORLD_ANVIL_APP_KEY")
        self.user_token = os.getenv("WORLD_ANVIL_USER_TOKEN")
        self.created_articles: list[str] = []
        self.test_results: dict[str, dict] = {}

        if not self.app_key or not self.user_token:
            raise ValueError(
                "Missing credentials: Set WORLD_ANVIL_APP_KEY and WORLD_ANVIL_USER_TOKEN"
            )

    async def run_all_tests(self) -> dict[str, dict]:
        """Execute full test suite.

        Returns:
            Test results dictionary with success/failure status
        """
        print("\n" + "=" * 60)
        print("World Anvil Live API Test Suite")
        print("=" * 60)
        print(f"World ID: {self.world_id}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 60 + "\n")

        async with WorldAnvilClient(
            api_key=self.app_key,
            user_token=self.user_token,
        ) as client:
            self.client = client

            # Test sequence
            await self._test_world_read()
            await self._test_article_create()
            await self._test_article_update()
            await self._test_article_read()
            await self._test_article_delete()
            await self._test_error_handling()
            await self._cleanup()

        self._print_summary()
        return self.test_results

    async def _test_world_read(self) -> None:
        """Validate world exists and is accessible."""
        print("📖 Test 1: World Read Access")
        print("-" * 60)

        try:
            world = await self.client.get_world(self.world_id, granularity="1")
            print(f"✅ World accessible: {world.get('name', 'N/A')}")
            print(f"   ID: {world.get('id')}")
            print(f"   Articles: {world.get('articleCount', 0)}")

            self.test_results["world_read"] = {
                "status": "PASS",
                "world_name": world.get("name"),
                "article_count": world.get("articleCount"),
            }
        except Exception as e:
            print(f"❌ World read failed: {e}")
            self.test_results["world_read"] = {"status": "FAIL", "error": str(e)}
            raise  # Stop if world not accessible

        print()

    async def _test_article_create(self) -> None:
        """Test article creation (PUT)."""
        print("➕ Test 2: Article Creation (PUT)")
        print("-" * 60)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        article_data = {
            "title": f"MCP-TEST-Article-{timestamp}",
            "content": "This is a test article created by the World Anvil MCP test suite.",
            "state": "draft",  # Use draft to avoid publishing
        }

        try:
            # Note: Exact endpoint and parameters may need adjustment based on API docs
            # This is a placeholder for the actual create article endpoint
            result = await self.client._request(
                method="PUT",
                endpoint=f"world/{self.world_id}/article",
                json=article_data,
            )

            article_id = result.get("id")
            if article_id:
                self.created_articles.append(article_id)
                print(f"✅ Article created successfully")
                print(f"   ID: {article_id}")
                print(f"   Title: {result.get('title')}")

                self.test_results["article_create"] = {
                    "status": "PASS",
                    "article_id": article_id,
                    "title": result.get("title"),
                }
            else:
                print("⚠️  Article created but no ID returned")
                self.test_results["article_create"] = {
                    "status": "PARTIAL",
                    "note": "No ID in response",
                }

        except WorldAnvilAPIError as e:
            print(f"❌ Article creation failed: {e}")
            print(f"   Status code: {e.status_code if hasattr(e, 'status_code') else 'N/A'}")
            self.test_results["article_create"] = {"status": "FAIL", "error": str(e)}

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.test_results["article_create"] = {
                "status": "FAIL",
                "error": f"Unexpected: {e}",
            }

        print()

    async def _test_article_update(self) -> None:
        """Test article update (PATCH)."""
        print("✏️  Test 3: Article Update (PATCH)")
        print("-" * 60)

        if not self.created_articles:
            print("⚠️  Skipped: No article created in previous test")
            self.test_results["article_update"] = {
                "status": "SKIP",
                "reason": "No article to update",
            }
            print()
            return

        article_id = self.created_articles[0]
        updated_content = "Updated content at " + datetime.now().isoformat()

        try:
            result = await self.client._request(
                method="PATCH",
                endpoint=f"world/{self.world_id}/article/{article_id}",
                json={"content": updated_content},
            )

            print(f"✅ Article updated successfully")
            print(f"   ID: {article_id}")
            print(f"   Updated content: {result.get('content', 'N/A')[:50]}...")

            self.test_results["article_update"] = {
                "status": "PASS",
                "article_id": article_id,
            }

        except Exception as e:
            print(f"❌ Article update failed: {e}")
            self.test_results["article_update"] = {"status": "FAIL", "error": str(e)}

        print()

    async def _test_article_read(self) -> None:
        """Validate article can be read after creation/update."""
        print("📖 Test 4: Article Read Verification")
        print("-" * 60)

        if not self.created_articles:
            print("⚠️  Skipped: No article to read")
            self.test_results["article_read"] = {
                "status": "SKIP",
                "reason": "No article created",
            }
            print()
            return

        article_id = self.created_articles[0]

        try:
            # Verify cache invalidation by reading back
            article = await self.client._request(
                method="GET",
                endpoint=f"world/{self.world_id}/article/{article_id}",
                params={"granularity": "1"},
            )

            print(f"✅ Article readable after update")
            print(f"   Title: {article.get('title')}")
            print(f"   State: {article.get('state', 'N/A')}")

            self.test_results["article_read"] = {
                "status": "PASS",
                "article_id": article_id,
                "title": article.get("title"),
            }

        except Exception as e:
            print(f"❌ Article read failed: {e}")
            self.test_results["article_read"] = {"status": "FAIL", "error": str(e)}

        print()

    async def _test_article_delete(self) -> None:
        """Test article deletion (DELETE)."""
        print("🗑️  Test 5: Article Deletion (DELETE)")
        print("-" * 60)

        if not self.created_articles:
            print("⚠️  Skipped: No article to delete")
            self.test_results["article_delete"] = {
                "status": "SKIP",
                "reason": "No article created",
            }
            print()
            return

        article_id = self.created_articles[0]

        try:
            await self.client._request(
                method="DELETE",
                endpoint=f"world/{self.world_id}/article/{article_id}",
            )

            print(f"✅ Article deleted successfully")
            print(f"   ID: {article_id}")

            # Verify deletion by attempting read
            try:
                await self.client._request(
                    method="GET",
                    endpoint=f"world/{self.world_id}/article/{article_id}",
                )
                print("⚠️  Article still readable after deletion (unexpected)")
                self.test_results["article_delete"] = {
                    "status": "PARTIAL",
                    "note": "Article still exists after DELETE",
                }
            except WorldAnvilNotFoundError:
                print("✅ Verified: Article returns 404 after deletion")
                self.test_results["article_delete"] = {
                    "status": "PASS",
                    "verified_404": True,
                }

            # Remove from cleanup list since deleted
            self.created_articles.remove(article_id)

        except Exception as e:
            print(f"❌ Article deletion failed: {e}")
            self.test_results["article_delete"] = {"status": "FAIL", "error": str(e)}

        print()

    async def _test_error_handling(self) -> None:
        """Test error scenarios."""
        print("🚨 Test 6: Error Handling")
        print("-" * 60)

        error_results = {}

        # Test 1: Invalid article ID (404)
        try:
            await self.client._request(
                method="GET",
                endpoint=f"world/{self.world_id}/article/invalid-id-12345",
            )
            error_results["404_handling"] = "FAIL - No 404 raised"
        except WorldAnvilNotFoundError:
            print("✅ 404 handling: Correctly raises NotFoundError")
            error_results["404_handling"] = "PASS"
        except Exception as e:
            print(f"⚠️  404 handling: Unexpected error: {e}")
            error_results["404_handling"] = f"PARTIAL - {type(e).__name__}"

        # Test 2: Invalid credentials (if safe to test)
        # Skipped to avoid account issues

        self.test_results["error_handling"] = error_results
        print()

    async def _cleanup(self) -> None:
        """Clean up any remaining test articles."""
        print("🧹 Cleanup")
        print("-" * 60)

        if not self.created_articles:
            print("✅ No cleanup needed")
            print()
            return

        print(f"Cleaning up {len(self.created_articles)} test article(s)...")

        for article_id in self.created_articles[:]:
            try:
                await self.client._request(
                    method="DELETE",
                    endpoint=f"world/{self.world_id}/article/{article_id}",
                )
                print(f"✅ Deleted article {article_id}")
                self.created_articles.remove(article_id)
            except Exception as e:
                print(f"⚠️  Failed to delete {article_id}: {e}")

        if self.created_articles:
            print(f"⚠️  {len(self.created_articles)} article(s) remain - manual cleanup needed")
        else:
            print("✅ All test articles cleaned up")

        print()

    def _print_summary(self) -> None:
        """Print test summary."""
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results.values() if r.get("status") == "PASS")
        failed = sum(1 for r in self.test_results.values() if r.get("status") == "FAIL")
        skipped = sum(
            1 for r in self.test_results.values() if r.get("status") == "SKIP"
        )

        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Skipped: {skipped}")
        print()

        for test_name, result in self.test_results.items():
            status = result.get("status", "UNKNOWN")
            symbol = {"PASS": "✅", "FAIL": "❌", "SKIP": "⚠️", "PARTIAL": "⚠️"}.get(
                status, "❓"
            )
            print(f"{symbol} {test_name}: {status}")

        print("=" * 60 + "\n")


async def main():
    """Main entry point."""
    # Configuration
    TEST_WORLD_ID = os.getenv("TEST_WORLD_ID")

    if not TEST_WORLD_ID:
        print("❌ Error: TEST_WORLD_ID environment variable required")
        print("\nUsage:")
        print("  export TEST_WORLD_ID=your-world-id")
        print("  export WORLD_ANVIL_APP_KEY=your-app-key")
        print("  export WORLD_ANVIL_USER_TOKEN=your-user-token")
        print("  python scripts/test_live_api.py")
        sys.exit(1)

    # Run tests
    tester = LiveAPITester(world_id=TEST_WORLD_ID)
    results = await tester.run_all_tests()

    # Exit code based on results
    failed = sum(1 for r in results.values() if r.get("status") == "FAIL")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    asyncio.run(main())
