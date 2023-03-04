# from django.test import TestCase

# Create your tests here.
import os

files = os.getcwd()
file = os.path.join(files,'telegram', 'img', 'mao.png')

retult = open(file, 'rb')

print(retult)