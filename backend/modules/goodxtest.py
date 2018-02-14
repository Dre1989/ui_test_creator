import errno
import glob
import json
import logging
import os
import sys
from random import *
import time

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

# Global variables
_modulename = 'goodxtest'
DATABASE = 'goodxtest'
SAVE_FOLDER = os.path.normpath(os.getcwd() + '/save_files/')

try:
    with open("settings.json") as settings_file:
        SETTINGS_FILE = json.load(settings_file)
except:
    raise Exception("NO SETTINGS JSON FILE FOUND")

# Class
class goodxtest():
    def __init__(self, parent, getDatabase):
        self._parent = parent
        self.getDatabase = getDatabase
        self.FileHandling = FileHandling()

    def getTestsCount(self, session):
        return len(os.listdir(os.path.normpath(SAVE_FOLDER + '/tests/')))

    def getSuitesCount(self, session):
        return len(os.listdir(os.path.normpath(SAVE_FOLDER + '/suites/')))

    def getTests(self, session):
        tests = []
        for file in os.listdir(os.path.normpath(SAVE_FOLDER + '/tests/')):
            tests.append({ 'name' : file[:-5], 'type': 'test'})
        return tests

    def getSuites(self, session):
        tests = []
        for file in os.listdir(os.path.normpath(SAVE_FOLDER + '/suites/')):
            tests.append({ 'name': file[:-5], 'type': 'suite'})
        return tests

    def getImages(self, session):
        images = []
        for file in os.listdir(os.path.normpath(SAVE_FOLDER + '/images/')):
            images.append({"name": file[:-4]})
        return images

    def saveTest(self, session, model):
        with self.FileHandling.safe_open_w(os.path.normpath(SAVE_FOLDER + '/tests/' + model['name'] + '.json')) as fp:
            json.dump(model, fp, indent=4)

    def saveTestSuite(self, session, model):
        with self.FileHandling.safe_open_w(os.path.normpath(SAVE_FOLDER + '/suites/' + model['name'] + '.json')) as fp:
            json.dump(model, fp, indent=4)

    def loadTestSuite(self, session, test_name):
        return self._load_test_suite(test_name)

    def _load_test_suite(self, test_name):
        json_data = open(os.path.normpath(SAVE_FOLDER + '/suites/' + test_name + '.json')).read()
        return json.loads(json_data)

    def loadTest(self, session, test_name):
        return self._load_test(test_name)

    def _load_test(self, test_name):
        json_data = open(os.path.normpath(SAVE_FOLDER + '/tests/' + test_name + '.json')).read()
        return json.loads(json_data)

    def runTestSuite(self, session, model):
        # sorted(list_to_be_sorted, key=lambda k: k['order'])
        # Load all the test before you begin to execute them. So that the tests are equally as fast.
        suite_results = []
        for index, test in enumerate(model['tests']):
            if test['type'] == 'suite':
                test_suite = self._load_test_suite(test['name'])
                suite_results.append({
                    "name": test_suite["name"],
                    "index": index,
                    "type": "suite",
                    "results": self.runTestSuite(session, test_suite)
                })
            elif test['type'] == 'test':
                test_ = self._load_test(test['name'])
                suite_results.append({
                    "name": test_["name"],
                    "index": index,
                    "type": "test",
                    "results": self._run_test(test_)
                })
        return suite_results

    def runTest(self, session, model):
        self._run_test(model)

    # def _run_test(self, model):
    #     test_result =  {
    #         "failed_actions": [],
    #         "success_actions": []
    #     }
    #     for index, action in enumerate(model['actions']):
    #         try:
    #             if action['action'] == 'click':
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     _click(os.path.normpath(os.getcwd() + '\\images\\' + action['data'] + '.png'))
    #             if action['action'] == 'r_click':
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     _rightClick(os.path.normpath(os.getcwd() + '\\images\\' + action['data'] + '.png'))
    #             if action['action'] == 'doubleclick':
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     _doubleClick(os.path.normpath(os.getcwd() + '\\images\\' + action['data'] + '.png'))
    #             if action['action'] == 'wait':
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     _wait(os.path.normpath(os.getcwd() + '\\images\\' + action['data'] + '.png'), int(action['delay']))
    #             if action['action'] == 'clickwait':
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     _click(_wait(os.path.normpath(os.getcwd() + '\\images\\' + action['data'] + '.png'), int(action['delay'])))
    #             if action['action'] == 'type':
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     pyautogui.typewrite(action['data'])
    #             if action['action'] == 'keycombo':
    #                 keys = action['data'].split('+')
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     pyautogui.hotkey(*keys)
    #             if action['action'] == 'keypress':
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     pyautogui.typewrite(action['data'])
    #             if action['action'] == 'close':
    #                 for k in range(int(action.get('repeat', '1') or '1')):
    #                     pyautogui.hotkey('alt', 'f4')
    #             test_result["success_actions"].append({
    #                 "index": index,
    #                 "action": action["action"],
    #                 "data": action["data"]
    #             })
    #         except Exception as ex:
    #             test_result["failed_actions"].append({
    #                 "index": index,
    #                 "action": action["action"],
    #                 "data": action["data"],
    #                 "error": str(ex.__doc__)
    #             })
    #     return test_result

    def searchTests(self, session, search_term):
        tests = self.getTests(session)
        tests_ = []
        for test in tests:
            if test['name'].lower().find(search_term.lower()) > -1:
                tests_.append(test)
        return tests_

    def searchSuites(self, session, search_term):
        suites = self.getSuites(session)
        suites_ = []
        for suite in suites:
            if suite['name'].lower().find(search_term.lower()) > -1:
                suites_.append(suite)
        return suites_

    def login(self, session, username, password):
        # Ensure the user is not logged in.
        if session is None:
            return self._parent.doLogin(DATABASE, username, password)

        # If the user is logged in , logout the user and login again with the new session id. This is 
        else:
            self._parent.doLogout()
            return self._parent.doLogin(DATABASE, username, password)

    def logout(self, session):
        if session is None:
            raise Exception('NOT LOGGED IN')
        else:
            return self._parent.doLogout()

    def getUser(self, session):
        return self._parent.getUser()

    def getLoggedIn(self, session):
        return self._parent.getLoggedIn()

class FileHandling:
    """
    Better why to handle files that needs to be saved etc.
    The function below safe_open() take a path and will check if path exist.
    If it doesn't, it will attempt to create the folders.
    EXAMPLE USAGE: with safe_open_w('/Users/bill/output/output-text.txt') as f:
                       f.write(stuff_to_file)
    """
    def _mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def safe_open_w(self, path):
        ''' Open "path" for writing, creating any parent directories as needed.
        '''
        self._mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def safe_create_path(self, path):
        '''Create Path give if doesn't exist
        '''
        self._mkdir_p(os.path.dirname(path))
        return path

class TestLoader:
    """
    Get test case/suite to load all data off.
    Get test actions, images (base64) and settings etc.
    Post everying to remote client in json.
    """
    def get_all_test_data(self, test_case_suite_name):
        jsonData = {}
        return jsonData


Module = goodxtest
