class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# For use on Heroku
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://uvyygsmbjrjsda:70dde68a91f363b964b2a581846c07d80284de8875af0fcb0dd7f6a053ca6d5f@ec2-54-146-84-101.compute-1.amazonaws.com:5432/dc9uf2dvu4i1t9'

# For use when developing on local machines
class DevelopmentConfig(Config):
    DEBUG = True
    # Change to local database
    SQLALCHEMY_DATABASE_URI = 'postgresql://bsamineni:@localhost/bsamineni'