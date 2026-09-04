import hashlib
import importlib.util
import json
import pathlib
import tarfile
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).parents[1] / "scripts" / "package_release.py"
SPEC = importlib.util.spec_from_file_location("package_release", MODULE_PATH)
package_release = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(package_release)


class PackageReleaseTests(unittest.TestCase):
    def test_bundle_is_deterministic_and_self_describing(self):
        with tempfile.TemporaryDirectory() as root:
            root = pathlib.Path(root)
            public = root / "public"
            public.mkdir()
            (public / "index.html").write_text("hello", encoding="utf-8")
            sha = "0123456789012345678901234567890123456789"
            first = root / "first"
            second = root / "second"
            a = package_release.build_bundle(public, first, "gnailuy/gnailuy.com", 42, sha, 123)
            b = package_release.build_bundle(public, second, "gnailuy/gnailuy.com", 42, sha, 123)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            manifest = json.loads((first / "manifest.json").read_text())
            self.assertEqual(manifest["head_sha"], sha)
            self.assertEqual(manifest["workflow_run_id"], 42)
            expected = hashlib.sha256(a.read_bytes()).hexdigest()
            self.assertTrue((first / f"{a.name}.sha256").read_text().startswith(expected))
            with tarfile.open(a, "r:gz") as archive:
                self.assertEqual(archive.getnames(), ["index.html"])

    def test_rejects_symlinks_and_invalid_sha(self):
        with tempfile.TemporaryDirectory() as root:
            root = pathlib.Path(root)
            public = root / "public"
            public.mkdir()
            (public / "index.html").write_text("ok", encoding="utf-8")
            with self.assertRaises(ValueError):
                package_release.build_bundle(public, root / "out", "r", 1, "short", 0)
            (public / "link").symlink_to("index.html")
            with self.assertRaises(ValueError):
                package_release.build_bundle(public, root / "out", "r", 1, "0" * 40, 0)


if __name__ == "__main__":
    unittest.main()
