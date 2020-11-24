from app import db
from app.models import BleData
from app.schemes import BleDataSchema
from sqlalchemy import func
from app.models import User


def create(new_data=None,new_user=None):
    if new_data:
        add_data=new_data
    else:
        add_data=new_user

    db.session.add(add_data)
    db.session.commit()    
    

def read(id=None, email=None, public_id=None, user=False, all_data=False, page=None, count=None):
    if user:
        if id:
            return User.query.filter_by(id=id).first()
        elif email:
            return User.query.filter_by(email=email).first()
        elif public_id:
            return User.query.filter_by(public_id=public_id).first()
        else:
            return User.query.all() 
    else:
        if all_data:
            return BleData.query.order_by(BleData.id.desc()).all()
        elif page and count:
            return BleData.query.order_by(BleData.id.desc()).paginate(page,count,error_out=False)
        else:
            return db.session.query(func.count(BleData.id)).scalar()


def update():
    pass


def delete(bledata=False, id_user=None):
    if bledata:
        try:
            num = db.session.query(BleData).delete()
            db.session.commit()
            return num
        except:
            db.session.rollback()
    else:
        try:
            user = db.session.query(User).filter(User.id==id_user).first()
            db.session.delete(user)
            db.session.commit()
            print(0)
            return True
        except Exception as err:
            print(err)
            db.session.rollback()
            return False