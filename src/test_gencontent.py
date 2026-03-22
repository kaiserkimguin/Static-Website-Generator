import unittest

from gencontent import extract_title

class TestGetContent(unittest.TestCase):
    def test_extract_title(self):
    
    # standard test

        md ='# ist bob' 
        header = extract_title(md)
        self.assertEqual(header, 'ist bob')

    # test zur funktion der Exception
        md =' # ist bob' 
        with self.assertRaises(Exception):
            extract_title(md)

    # multiline test 1
        md ='abc \n# ist bob\n wasserkopf' 
        header = extract_title(md)
        self.assertEqual(header, 'ist bob')

    # multilinetest 2
        md ='''hallo
mein name
# ist bob'''
        header = extract_title(md)
        self.assertEqual(header, 'ist bob')

    # test mit mehreren h1 headern
        md ='''hallo
mein name
# ist bob
# ist nicht bob'''
        header = extract_title(md)
        self.assertEqual(header, 'ist bob')

    # test mit h2 header statt h1
        md ='## ist bob' 
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()