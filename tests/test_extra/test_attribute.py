"""Test attribute selectors."""
import time
import soupsieve as sv
from .. import util


class TestAttribute(util.TestCase):
    """Test attribute selectors."""

    MARKUP = """
    <div id="div">
    <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
    <a id="2" href="http://google.com">Link</a>
    <span id="3">Direct child</span>
    <pre id="pre">
    <span id="4">Child 1</span>
    <span id="5">Child 2</span>
    <span id="6">Child 3</span>
    </pre>
    </div>
    """

    def test_attribute_not_equal_no_quotes(self):
        """Test attribute with value that does not equal specified value (no quotes)."""

        # No quotes
        self.assert_selector(
            self.MARKUP,
            'body [id!=\\35]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_not_equal_quotes(self):
        """Test attribute with value that does not equal specified value (quotes)."""

        # Quotes
        self.assert_selector(
            self.MARKUP,
            "body [id!='5']",
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_not_equal_double_quotes(self):
        """Test attribute with value that does not equal specified value (double quotes)."""

        # Double quotes
        self.assert_selector(
            self.MARKUP,
            'body [id!="5"]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_bad_attribute_unclused(self):
        """Test bad attribute fails for syntax error, not timeout error."""

        # An attribute selector whose quoted value is never closed must fail fast with
        # a syntax error. The value pattern used to nest a quantifier inside a lazy
        # repeat (`[^\\"\r\n\f]+)*?`), which caused catastrophic backtracking: a value
        # of only a few hundred characters stalled the parser for seconds, and each
        # extra character multiplied the time.
        #
        # Elapsed time is measured rather than using `signal.alarm`, which does not
        # exist on Windows.
        for selector in ('[a="' + ('x' * 300), "[a='" + ('x' * 300)):
            self.purge()
            start = time.perf_counter()
            with self.assertRaises(sv.SelectorSyntaxError):
                sv.compile(selector)
            elapsed = time.perf_counter() - start
            self.assertLess(
                elapsed,
                3,
                'Compiling {!r}... took {:.3f}s, expected an immediate syntax error'.format(selector[:6], elapsed)
            )
