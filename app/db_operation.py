from app import db
from app.models import BleData
from app.schemes import BleDataSchema
from sqlalchemy import func
from app.models import User


def create(new_data=None,new_user=None):
    # new data
    if new_data:
        add_data=new_data
    # new user
    else:
        add_data=new_user

    db.session.add(add_data)
    db.session.commit()    
    

def read(id=None, email=None, public_id=None, user=False, all_data=False, page=None, count=None):
    if user:
        if id:
            # get user by id
            return User.query.filter_by(id=id).first()
        elif email:
            # get user by email
            return User.query.filter_by(email=email).first()
        elif public_id:
            # get user by pyblic_id
            return User.query.filter_by(public_id=public_id).first()
        else:
            # get all user
            return User.query.all() 
    else:
        if all_data:
            # get all data
            return BleData.query.order_by(BleData.id.desc()).all()
        elif page and count:
            # get data with pagination
            return BleData.query.order_by(BleData.id.desc()).paginate(page,count,error_out=False)
        else:
            # get number of records data
            return db.session.query(func.count(BleData.id)).scalar()


def update(field, new_value, current_user):
    # try update field with new value
    try:
        User.query.filter_by(id=current_user.id).update({field:new_value})
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def delete(bledata=False, id_user=None):
    if bledata:
        # try delete all data
        try:
            num = db.session.query(BleData).delete()
            db.session.commit()
            return num
        except:
            db.session.rollback()
    else:
        # try delete user by id
        try:
            user = db.session.query(User).filter(User.id==id_user).first()
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as err:
            db.session.rollback()
            return False