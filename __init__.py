# Copyright 2019 rekkitcwts
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import feedparser
import re
import os
import subprocess
import sqlite3

from adapt.intent import IntentBuilder
from mycroft.audio import wait_while_speaking
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.skills.context import adds_context, removes_context
import traceback
from requests import Session

import urllib, json
import requests
from urllib.request import urlopen


# A template for skills that require a local storage like SQLITE

# The class BufordSQLite that handles the sqlite database in an OOP manner
# Named to avoid confusion with the built-in SQLite libraries
class BufordSQLite:
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        # Use any name that you want here
        # TODO - this saves to the mycroft-core directory by default
        self.conn = sqlite3.connect('buford.db')

    # Query that returns nothing (e.g. INSERT)
    def emptyQuery(self, query):
        self.conn.execute(query)

    # Query that returns something. Accepted Values - Single (1R x 1C), Columns(1R x nC), Table (nR x nC)
    def returnQuery(self, query, return_type="Single"):
        if return_type == "Single":
            return self.conn.execute(query).fetchone()[0] # Returns a single object
        if return_type == "Columns":
            return self.conn.execute(query).fetchone() # Returns a row
        if return_type == "Table":
            return self.conn.execute(query).fetchall() # Returns a n x n table

    # Required in order to make changes to database
    def commit(self):
        self.conn.commit()

    # Closes Database Connection
    def close(self):
        self.conn.close()
        

class SQLiteDemoSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(SQLiteDemoSkill, self).__init__(name="SQLiteDemoSkill")
        
        # TODO: Initialize working variables used within the skill.

    # Runs the SQLite Demo
    @intent_handler(IntentBuilder("RunSQLiteDemoIntent").require("Demo"))
    def handle_sqlite_demo_intent(self, message):
        self.speak("Running the SQLite Demo")
        conn = BufordSQLite()
        tablequery = "CREATE TABLE IF NOT EXISTS names (first_name TEXT, last_name TEXT)"
        insertquery = "INSERT INTO names (first_name, last_name) VALUES ('Reinhardt', 'Wilhelm')"
        insertquery2 = "INSERT INTO names (first_name, last_name) VALUES ('Amelie', 'Lacroix')"
        self.speak("Creating the database file and table")
        conn.emptyQuery(tablequery)
        self.speak("Inserting two entries to the table")
        conn.emptyQuery(insertquery)
        conn.emptyQuery(insertquery2)
        self.speak("Saving changes")
        conn.commit()
        self.speak("Printing one cell: " + conn.returnQuery("SELECT * FROM names"))
        one_name = conn.returnQuery("SELECT * FROM names", "Columns")
        one_table = conn.returnQuery("SELECT * FROM names", "Table")
        self.speak("Printing one row: " + one_name[0] + " " + one_name[1])
        self.speak("Closing the database connection")
        conn.close()
        self.speak("SQLite demo complete")

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return SQLiteDemoSkill()
