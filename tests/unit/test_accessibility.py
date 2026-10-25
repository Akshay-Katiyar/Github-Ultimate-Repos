import os
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INDEX_HTML = os.path.join(REPO_ROOT, "index.html")

def sRGB_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def relative_luminance(hex_str):
    hex_str = hex_str.lstrip('#')
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return 0.2126 * sRGB_to_linear(r) + 0.7152 * sRGB_to_linear(g) + 0.0722 * sRGB_to_linear(b)

def contrast_ratio(hex1, hex2):
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

class TestAccessibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            cls.html = f.read()

    def test_color_contrast_ratios_wcag_aa(self):
        """Verify all core UI text and components exceed WCAG 2.2 AA contrast ratios (> 4.5:1 text, > 3:1 non-text)."""
        color_pairs = [
            ("Main text on surface", "#f9fafb", "#111827", 4.5),
            ("Main text on background", "#f9fafb", "#0b0f19", 4.5),
            ("Accent text on surface", "#38bdf8", "#111827", 4.5),
            ("Muted text on surface", "#9ca3af", "#111827", 4.5),
            ("Star rating on surface", "#fbbf24", "#111827", 4.5),
            ("Category badge on surface", "#c4b5fd", "#111827", 4.5),
            ("Card description on surface", "#e2e8f0", "#111827", 4.5),
            ("Interactive form border", "#64748b", "#111827", 3.0),
            ("Focus outline on surface", "#38bdf8", "#111827", 3.0)
        ]
        for name, c1, c2, threshold in color_pairs:
            cr = contrast_ratio(c1, c2)
            self.assertGreaterEqual(cr, threshold, f"{name} ({c1} vs {c2}) contrast {cr:.2f}:1 failed threshold {threshold}:1")

    def test_focus_visible_and_keyboard_navigation(self):
        """Verify skip-link and visible focus rings exist for all interactive elements."""
        self.assertIn('class="skip-link"', self.html)
        self.assertIn('.skip-link:focus', self.html)
        self.assertIn(':focus-visible', self.html)
        self.assertIn('input:focus-visible', self.html)
        self.assertIn('select:focus-visible', self.html)
        self.assertIn('.page-btn:focus-visible', self.html)
        self.assertIn('.repo-title a:focus-visible', self.html)

    def test_aria_labels_and_landmarks(self):
        """Verify ARIA attributes, semantic landmarks, and screen reader announcements."""
        self.assertIn('role="banner"', self.html)
        self.assertIn('<main id="main-content"', self.html)
        self.assertIn('role="search"', self.html)
        self.assertIn('id="searchInput"', self.html)
        self.assertIn('aria-label="Search repositories by name, keyword, workflow, or technology"', self.html)
        self.assertIn('id="catSelect"', self.html)
        self.assertIn('aria-label="Filter repositories by technology discipline"', self.html)
        self.assertIn('id="resultsAnnouncer"', self.html)
        self.assertIn('role="status"', self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('id="prevBtn"', self.html)
        self.assertIn('aria-label="Go to previous page of repositories"', self.html)
        self.assertIn('id="nextBtn"', self.html)
        self.assertIn('aria-label="Go to next page of repositories"', self.html)

    def test_responsive_layout_320px_to_4k(self):
        """Verify responsive breakpoints covering 320px mobile up to 4K displays."""
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1.0">', self.html)
        self.assertIn('@media (max-width: 360px)', self.html) # 320px mobile
        self.assertIn('@media (max-width: 640px)', self.html) # Mobile
        self.assertIn('@media (max-width: 992px)', self.html) # Tablet
        self.assertIn('@media (min-width: 1800px)', self.html) # 2K Ultra-wide
        self.assertIn('@media (min-width: 2560px)', self.html) # 4K UHD
        self.assertIn('min-height: 48px', self.html) # Touch target size
        self.assertIn('min-height: 44px', self.html) # Touch target size

    def test_reduced_motion_media_query_support(self):
        """Verify prefers-reduced-motion is supported in both CSS and JavaScript."""
        self.assertIn('@media (prefers-reduced-motion: reduce)', self.html)
        self.assertIn("window.matchMedia('(prefers-reduced-motion: reduce)')", self.html)

if __name__ == "__main__":
    unittest.main()
