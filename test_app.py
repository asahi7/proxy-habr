import unittest
import app

class AppTest(unittest.TestCase):


    def test_swap_habr_links(self):
        link = 'http://127.0.0.1:8232'
        html_text = '<b><a href="https://habrahabr.ru/ru/company/yandex/blog/258673/">Yandex</a></b>'
        expected_html_text = '<b><a href="http://127.0.0.1:8232/ru/company/yandex/blog/258673/">Yandex</a></b>'
        self.assertEqual(app.swap_habr_links(html_text, link), expected_html_text)
        self.assertEqual(app.swap_habr_links('https://habr.com/hello/world/1', link), 'http://127.0.0.1:8232/hello/world/1')
        self.assertEqual(app.swap_habr_links('https://habr.com/hello/world/1/', link), 'http://127.0.0.1:8232/hello/world/1/')
        self.assertEqual(app.swap_habr_links('https://habrahabr.ru/hello/world/1', link), 'http://127.0.0.1:8232/hello/world/1')
        self.assertEqual(app.swap_habr_links('http://habrahabr.ru/hello/world/1', link), 'http://127.0.0.1:8232/hello/world/1')
        self.assertEqual(app.swap_habr_links('http://habr.com/hello/world/1', link), 'http://127.0.0.1:8232/hello/world/1')
        self.assertEqual(app.swap_habr_links('https://habr.com', link), 'http://127.0.0.1:8232')
        self.assertEqual(app.swap_habr_links('http://example.com', link), 'http://example.com')
        self.assertEqual(app.swap_habr_links('', link), '')
        self.assertEqual(app.swap_habr_links('https://HABR.COM', link), 'http://127.0.0.1:8232')
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
        self.assertEqual(app.swap_habr_links(multiline_html, link), expected_multiline)


    def test_append_tm(self):
        self.assertEqual(app.append_tm('<b>Online<i>Worlds<p>Locals</p></i></b>'), '<b>Online™<i>Worlds™<p>Locals™</p></i></b>')
        self.assertEqual(app.append_tm('<b>Online<i>World<p>Locals</p></i></b>'),
                         '<b>Online™<i>World<p>Locals™</p></i></b>')
        self.assertEqual(app.append_tm('<body>Online</body>'), '<body>Online™</body>')
        self.assertEqual(app.append_tm('<body>Hello</body>'), '<body>Hello</body>')
        self.assertEqual(app.append_tm('<body>Good friend!</body>'), '<body>Good friend™!</body>')
        self.assertEqual(app.append_tm('<svg>Good friend!</svg>'), '<svg>Good friend!</svg>')

if __name__ == '__main__':
    unittest.main()