import unittest

from app.tests.entry_routes.category.test_create_category import TestCreateCategory
from app.tests.entry_routes.category.test_delete_category import TestDeleteCategory
from app.tests.entry_routes.category.test_get_category import TestGetCategory
from app.tests.entry_routes.category.test_update_category import TestUpdateCategory
from app.tests.entry_routes.habit.test_create_habit import TestCreateHabit
from app.tests.entry_routes.habit.test_delete_habit import TestDeleteHabit
from app.tests.entry_routes.habit.test_get_habit import TestGetHabit
from app.tests.entry_routes.habit.test_update_habit import TestUpdateHabit
from app.tests.entry_routes.journal.test_create_journal import TestCreateJournal
from app.tests.entry_routes.journal.test_delete_journal import TestDeleteJournal
from app.tests.entry_routes.journal.test_get_journal import TestGetJournal
from app.tests.entry_routes.journal.test_update_journal import TestUpdateJournal
from app.tests.entry_routes.todo.test_create_todo import TestCreateToDo
from app.tests.entry_routes.todo.test_delete_todo import TestDeleteToDo
from app.tests.entry_routes.todo.test_get_todo import TestGetToDo
from app.tests.entry_routes.todo.test_update_todo import TestUpdateToDo
from app.tests.entry_routes.topic.test_create_topic import TestCreateTopic
from app.tests.entry_routes.topic.test_delete_topic import TestDeleteTopic
from app.tests.entry_routes.topic.test_get_topic import TestGetTopic
from app.tests.entry_routes.topic.test_update_topic import TestUpdateTopic
from app.tests.user_routes.test_create_user import TestCreateUser
from app.tests.user_routes.test_delete_user import TestDeleteUser
from app.tests.user_routes.test_email_verification import TestEmailVerification
from app.tests.user_routes.test_get_token import TestGetToken
from app.tests.user_routes.test_get_user import TestGetUser
from app.tests.user_routes.test_password_reset import TestPasswordReset
from app.tests.user_routes.test_update_password import TestUpdatePassword
from app.tests.user_routes.test_update_user import TestUpdateUser

if __name__ == '__main__':
    unittest.main()
