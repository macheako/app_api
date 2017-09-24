#!/usr/bin/env python
# encoding: utf-8

import sys
import cherrypy
import threading
import time
import logging

import peewee
from peewee import *

class User(peewee.Model):