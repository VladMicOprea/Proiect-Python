from Tests.testDomain import testDomain
from Tests.testRepository import testRepository
from Tests.testService import testService


def testAll():
    testDomain()
    testRepository()
    testService()
