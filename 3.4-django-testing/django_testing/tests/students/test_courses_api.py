import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Student, Course
@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def path():
    return 'http://127.0.0.1:8000/api/v1/courses/'

@pytest.fixture
def student():
    return Student.objects.create(name='Tester', birth_date='1996-07-15')

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory
@pytest.mark.django_db
def test_first_course(client, course_factory, path):
    # Arrange
    courses = course_factory(_quantity=10)
    # Act
    course_id = courses[0].id
    response = client.get(path + str(course_id) + '/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses[0].name

@pytest.mark.django_db
def test_courses(client, course_factory, path):
    # Arrange
    courses = course_factory(_quantity=15)
    # Act
    response = client.get(path)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)

@pytest.mark.django_db
def test_course_filter_id(client, course_factory, path):
    # Arrange
    courses = course_factory(_quantity=10)
    # Act
    course_id = courses[5].id
    response = client.get(path + '?id=' + str(course_id))
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course_id

@pytest.mark.django_db
def test_course_filter_name(client, course_factory, path):
    # Arrange
    courses = course_factory(_quantity=10)
    # Act
    course_name = courses[3].name
    response = client.get(path + '?name=' + course_name)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course_name

@pytest.mark.django_db
def test_course_create(client, path):
    # Arrange
    name_course = 'Test1'
    # Act
    response = client.post(path, data={'name': name_course})
    # Assert
    assert response.status_code == 201
    response = client.get(path + '?name=' + name_course)
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == name_course

@pytest.mark.django_db
def test_course_update(client, course_factory, path):
    # Arrange
    courses = course_factory(_quantity=1)
    second_name = 'Test1'
    # Act
    response = client.patch(path + str(courses[0].id) + '/', data={'name': second_name})
    # Assert
    assert response.status_code == 200
    response = client.get(path + '?name=' + second_name)
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == second_name

@pytest.mark.django_db
def test_course_delete(client, course_factory, path):
    # Arrange
    courses = course_factory(_quantity=1)
    course_id = courses[0].id
    # Act
    response = client.delete(path + str(course_id) + '/')
    # Assert
    assert response.status_code == 204
    response = client.get(path)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

