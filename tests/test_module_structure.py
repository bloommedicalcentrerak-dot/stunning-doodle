from pathlib import Path
import unittest


class OdooModuleStructureTest(unittest.TestCase):
    def test_odoo_addon_lives_under_bloom_os_directory(self):
        repo_root = Path(__file__).resolve().parents[1]
        addon_root = repo_root / 'bloom_os'

        self.assertTrue(addon_root.is_dir())
        self.assertTrue((addon_root / '__init__.py').is_file())
        self.assertTrue((addon_root / '__manifest__.py').is_file())
        self.assertTrue((addon_root / 'models' / '__init__.py').is_file())
        self.assertTrue((addon_root / 'security' / 'ir.model.access.csv').is_file())
        self.assertTrue((addon_root / 'views').is_dir())

        self.assertFalse((repo_root / '__manifest__.py').exists())
        self.assertFalse((repo_root / 'models').exists())
        self.assertFalse((repo_root / 'views').exists())


if __name__ == '__main__':
    unittest.main()
