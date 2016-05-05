from sqlalchemy import create_engine
engine = create_engine('mysql://journals:journals@127.0.0.1:3306/journals?charset=utf8')
