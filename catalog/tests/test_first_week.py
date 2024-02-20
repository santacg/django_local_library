"""
First Week Tests
Created by JAMI
EPS-UAM 2024
"""

import sys
import os
from django.test import TestCase

from catalog.models import Book, BookInstance, Language, Genre, Author

def check_environment():
    """ Check if we are using a python defined in a virtual enviroment
    or in a conda enviroment different from 'base'"""
    result = False
    # Check if we are inside a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        result = True
   # check if we are inside a conda environment different from base
    elif os.environ.get('CONDA_DEFAULT_ENV') is not None:
        if os.environ.get('CONDA_DEFAULT_ENV') != 'base':
            result = True
    return result
    
class FirstWeekTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        try:
            from populate_catalog import populate
            populate()
        except ImportError:
            print('The module populate_catalog does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except Exception:
            print('Something went wrong in the populate() function :-(')
            raise


    def test_running_inside_virtualenv(self):
       vi_on = check_environment()
       self.assertTrue(vi_on)


    def test_admin_pattern(self):
        try:
            from locallibrary.urls import urlpatterns as urlp
            self.assertIn('admin', str(urlp[0]))
        except Exception:
            print('Did you define urlpatterns? Something is wrong with that!')
            raise


    def test_catalog_pattern(self):
        try:
            from locallibrary.urls import urlpatterns as urlp
            self.assertIn('catalog.urls', str(urlp[1]))
        except Exception:
            print('Did you define urlpatterns? Something is wrong with that!')
            raise


    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'birth') 


    def test_booK_with_two_genres(self):
        book = Book.objects.get(id=1)
        self.assertTrue((book.genre.count()>= 2))


    def test_due_back_book_on_loan(self):
        bi = BookInstance.objects.filter(book__title='The Shining', status='o').first()
        self.assertEqual(str(bi.due_back), '2021-10-10')


    def test_books_on_loan(self):
        bi = BookInstance.objects.filter(status='o').count()
        self.assertTrue((bi>=2))


    def test_challenge_one_1(self):
        try:
            l1 = language = Language.objects.filter(name__contains='English').first()
            fl = l1._meta.get_field('name').verbose_name
            self.assertEqual(fl, 'name')
        except Exception:
            print('Did you work on the Language Model Challenge? Something is wrong with that!')
            raise


    def test_challenge_one_2(self):
        try:
            l1 = language = Language.objects.filter(name__contains='English').values()[0]['name']
            self.assertEqual(l1, 'English')
        except Exception:
            print('Did you work on the Language Model Challenge? Something is wrong with that!')
            raise


    def test_challenge_one_3(self):
        try:
            l2 = language = Language.objects.filter(name__contains='Spanish').values()[0]['name']
            self.assertEqual(l2, 'Spanish')
        except Exception:
            print('Did you work on the Language Model Challenge? Something is wrong with that!')
            raise
