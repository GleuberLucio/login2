
class Config:
    """Base configuration class."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = b'1fa62e99a79097d1a3d1f6f0926076056ca898d3cdb820530246c2a2a893a7d0'