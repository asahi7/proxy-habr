import unittest
import app


class AppTest(unittest.TestCase):

    def test_swap_habr_links(self):
        link = 'http://127.0.0.1:8232'
        html_text = '<b><a href="https://habrahabr.ru/ru/company/yandex/blog/258673/">Yandex</a></b>'
        expected_html_text = '<b><a href="http://127.0.0.1:8232/ru/company/yandex/blog/258673/">Yandex</a></b>'
        self.assertEqual(
            app.swap_habr_links(
                html_text,
                link),
            expected_html_text)
        self.assertEqual(
            app.swap_habr_links(
                'https://habr.com/hello/world/1',
                link),
            'http://127.0.0.1:8232/hello/world/1')
        self.assertEqual(
            app.swap_habr_links(
                'https://habr.com/hello/world/1/',
                link),
            'http://127.0.0.1:8232/hello/world/1/')
        self.assertEqual(
            app.swap_habr_links(
                'https://habrahabr.ru/hello/world/1',
                link),
            'http://127.0.0.1:8232/hello/world/1')
        self.assertEqual(
            app.swap_habr_links(
                'http://habrahabr.ru/hello/world/1',
                link),
            'http://127.0.0.1:8232/hello/world/1')
        self.assertEqual(
            app.swap_habr_links(
                'http://habr.com/hello/world/1',
                link),
            'http://127.0.0.1:8232/hello/world/1')
        self.assertEqual(
            app.swap_habr_links(
                'https://habr.com',
                link),
            'http://127.0.0.1:8232')
        self.assertEqual(
            app.swap_habr_links(
                'http://example.com',
                link),
            'http://example.com')
        self.assertEqual(app.swap_habr_links('', link), '')
        self.assertEqual(
            app.swap_habr_links(
                'https://HABR.COM',
                link),
            'http://127.0.0.1:8232')
        multiline_html = '''
        <div>
        <a href="https://habr.com/hello/world">Hello world</a>
        <a href="http://habrahabr.ru/hello/world">Hello world 2</a>
        </div>
        '''
        expected_multiline = '''
        <div>
        <a href="http://127.0.0.1:8232/hello/world">Hello world</a>
        <a href="http://127.0.0.1:8232/hello/world">Hello world 2</a>
        </div>
        '''
        self.assertEqual(
            app.swap_habr_links(
                multiline_html,
                link),
            expected_multiline)

    def test_append_tm(self):
        self.assertEqual(
            app.append_tm('<b>Online<i>Worlds<p>Locals</p></i></b>'),
            '<html><head></head><body><b>Online™<i>Worlds™<p>Locals™</p></i></b></body></html>')
        self.assertEqual(
            app.append_tm('<b>Online<i>World<p>Locals</p></i></b>'),
            '<html><head></head><body><b>Online™<i>World<p>Locals™</p></i></b></body></html>')
        self.assertEqual(
            app.append_tm('<body>Online</body>'),
            '<html><head></head><body>Online™</body></html>')
        self.assertEqual(
            app.append_tm('<body>Hello</body>'),
            '<html><head></head><body>Hello</body></html>')
        self.assertEqual(
            app.append_tm('<body>Good friend!</body>'),
            '<html><head></head><body>Good friend™!</body></html>')
        self.assertEqual(
            app.append_tm('<svg>Good friend!</svg>'),
            '<html><head></head><body><svg>Good friend!</svg></body></html>')
        self.assertEqual(
            app.append_tm('<section><div><!-- /235032688/HH/HH01_ATF_Poster --></div></section>'),
            '<html><head></head><body><section><div><!-- /235032688/HH/HH01_ATF_Poster --></div></section></body></html>')
        self.assertEqual(app.append_tm('<b>&pound;682m</b>'),
                         '<html><head></head><body><b>£682m</b></body></html>')
        self.assertEqual(app.append_tm('<b>&plus;</b>'),
                         '<html><head></head><body><b>+</b></body></html>')
        self.assertEqual(app.append_tm('<b>&plus;53</b>'),
                         '<html><head></head><body><b>+53</b></body></html>')


if __name__ == '__main__':
    unittest.main()
