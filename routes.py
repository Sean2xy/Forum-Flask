from flask import render_template,redirect,jsonify,request,session,url_for
from flask import Flask
from init_db import conn,cursor
from params_req import BaseResponseParams
from datetime import datetime
import hashlib

app = Flask(
    __name__,
)

app.secret_key = "a new web"
app.jinja_env.auto_reload = True

PAGE = 4

class BaseResponse(object):
    user_account = ['common', 'admin']

    session_key = "session_key"

    def __init__(self):
        app.add_template_global(self.session_login,"login")

    def response(self,code=0,message="ok"):
        return jsonify({
            "status" : code,
            "msg" : message
        })

    def change_datetime(self,data,key=""):
        format = "%Y-%m-%dT%H:%M:%S"
        if type(data) == list:
            for index,li in enumerate(data):
                data[index][key] = li[key].strftime(format)
        elif type(data) == dict:
            data[key].strftime(format)
        elif not data:
            return data
        else:
            return data.strftime(format)
        return data

    def session_add(self,user):
        session[self.session_key] = user

    def session_login(self):
        try:
            user = session[self.session_key]
            assert user
            return True
        except Exception as e:
            pass
        return False
    def session_uid(self):
        try:
            user = session[self.session_key]
            return user["id"]
        except Exception as e:
            pass
        return -1
    def session_logout(self):
        try:
            del session[self.session_key]
        except Exception as e:
            pass
response = BaseResponse()

def check_login_status(func):
    def wrapper(*args, **kwargs):
        if response.session_login():
            return func(*args, **kwargs)
        else:
            return response.response(51,"please login....")

    wrapper.__name__ = func.__name__
    return wrapper

def md5_set(value):
    md5 = hashlib.md5()
    md5.update(bytes(str(value),encoding="utf8"))
    hash_code = md5.hexdigest()
    return str(hash_code).lower()
def md5_match(value,password):
    value = md5_set(value)
    return value == password

@app.route("/user_login",methods=["POST"])
def user_login():
    requests = BaseResponseParams(request)
    username = requests.username
    password = requests.password
    print(username,password)

    if not username or not password:
        return response.response(3,"username or passowrd not empty !")

    try:
        sql = "select * from user where user_name=%s and user_passworld=%s"
        cursor.execute(sql, (username,md5_set(password)))
        data = cursor.fetchone()
        print("data: 111",data)
        assert data
        response.session_add(data)
    except Exception as e:
        print("e: ",e)
        return response.response(1,"user not exists ...")

    return response.response()

@app.route("/user_register",methods=["POST"])
def user_register():
    requests = BaseResponseParams(request)
    username = requests.username
    password = requests.password

    if not username or not password:
        return response.response(3,"username or passowrd not empty !")

    try:
        sql = "select * from user where user_name=%s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            return response.response(1,"user exists. ...")
        sql = "insert into user (user_name,user_passworld) VALUES (%s,%s)"
        cursor.execute(sql, (username,md5_set(password)))
        data = conn.commit()
        print("data: ",data)
    except Exception as e:
        print("register err: ",e)
        return response.response(2,"register failed")

    return response.response()

@app.route("/add_topic",methods=["POST"])
@check_login_status
def add_topic():
    requests = BaseResponseParams(request)
    topic = requests.topic

    if not topic:
        return response.response(10,"topic not empty .....")

    try:
        sql = "insert into topic (title,time,user_id) VALUES (%s,%s,%s)"
        cursor.execute(sql, (topic,datetime.now(),response.session_uid()))
        data = conn.commit()
    except Exception as e:
        return response.response(5,"topic add error .")

    return response.response()

@app.route("/",methods=["GET"])
@app.route("/home",methods=["GET","POST"])
def home():
    requests = BaseResponseParams(request)
    page = requests.page_int if requests.page_int else 1
    search_topic = requests.search_topic
    print("page: ",page)
    if search_topic:
        sql = f"select count(id) as count from topic where title like '%{search_topic}%'"
    else:
        sql = "select count(id) as count from topic"
    cursor.execute(sql)
    count = cursor.fetchone()["count"]
    print("count: ",count)

    pl,pr = divmod(count,PAGE)
    if pr:
        pl += 1
    if page > count or page < 1:
        page = 1

    prev_page = "javascript:;" if page <= 1 else url_for("home",page=page-1,search_topic=search_topic)
    next_page = "javascript:;" if page >= pl else url_for("home",page=page + 1,search_topic=search_topic)

    if search_topic:
        print("--------->>>")
        sql = f"select top.id,top.time,top.title,u.user_name" \
              f" from topic as top inner join user" \
              f" as u where top.user_id = u.id " \
              f"and top.title like '%{search_topic}%' limit {PAGE} offset {(page - 1)*PAGE}"
        # f"and top.title like '%{search_topic}%' limit %s offset %s"
        print("SQL: ",sql)
        # cursor.execute(sql,(PAGE,(page - 1) * PAGE))
        cursor.execute(sql)
        print("=LLLLLLL")
    else:
        sql = "select top.id,top.time,top.title,u.user_name from topic as top inner join user as u where top.user_id = u.id limit %s offset %s"
        cursor.execute(sql,(PAGE,(page - 1) * PAGE))
    data = cursor.fetchall()
    data = response.change_datetime(data,"time")
    print(data)
    params = {
        "prev_page" : prev_page,
        "next_page" : next_page,
        "data" : data,
        "requests":requests,
    }

    return render_template("index.html",**params)

@app.route("/add_claim",methods=["POST"])
def add_claim():
    requests = BaseResponseParams(request)
    claim = requests.claim
    topic_id = requests.topic_id
    get_params = requests.get_params()

    claim_attr_list = []
    key = "claim_"
    for k,v in get_params.items():
        k = str(k)
        if not k.startswith(key):
            continue
        if v == "opposed":
            claim_attr_list.append([k.lstrip(key),"opposed"])
        elif v == "equivalent":
            claim_attr_list.append([k.lstrip(key), "equivalent"])

    if not claim:
        return response.response(10,"claim not empty .....")

    try:
        print("NID: ",response.session_uid(),topic_id)
        sql = "insert into claim (heading,user_id,topic_id,time) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (claim,response.session_uid(),topic_id,datetime.now()))
        data = conn.commit()

        if claim_attr_list:
            sql = "insert into claim_relation (claim_id_2,type,claim_id_1) values (%s,%s,%s)"
            val = [[x,y,cursor.lastrowid] for x,y in claim_attr_list]
            cursor.executemany(sql,val)
            data = conn.commit()
    except Exception as e:
        print(e)
        return response.response(5,"claim add error .")

    return response.response()

@app.route("/claim/<claim_id>")
def claim(claim_id):
    requests = BaseResponseParams(request)
    page = requests.page_int if requests.page_int else 1

    data = []
    sql = "select * from claim"
    cursor.execute(sql)
    claim_list = cursor.fetchall()
    claim_list = response.change_datetime(claim_list,"time")

    sql = "select count(id) as count from claim where topic_id = %s"
    cursor.execute(sql,(claim_id,))
    count = cursor.fetchone()["count"]
    pl,pr = divmod(count,PAGE)
    if pr:
        pl += 1
    if page > count or page < 1:
        page = 1

    prev_page = "javascript:;" if page <= 1 else url_for("claim",claim_id=claim_id,page=page-1)
    next_page = "javascript:;" if page >= pl else url_for("claim",claim_id=claim_id,page=page + 1)

    try:
        sql = "select claim.id,claim.time,claim.heading,user.user_name from claim inner join topic inner join user where " \
              "topic.id = claim.topic_id and claim.user_id = user.id and  " \
              "topic.id=%s  limit %s offset %s"
        cursor.execute(sql,(claim_id,PAGE,(page - 1) * PAGE))
        data = cursor.fetchall()
    except Exception as e:
        print(e)
        pass
    
    data = response.change_datetime(data,"time")
    print("data: ",data)

    return render_template("claims.html",
                               data=data,claim_list=claim_list,
                               claim_id=claim_id,
                               prev_page=prev_page,
                               next_page=next_page,
                           )

@app.route("/add_reply",methods=["POST"])
def add_reply():
    # requests.args.get(claim_id,"") #get post
    requests = BaseResponseParams(request)
    reply_detail = requests.reply_detail
    claim_id = requests.claim_id
    reply_id = requests.reply_id
    claim_select = requests.claim
    reply_select = requests.reply
    print(requests.get_params())

    if not reply_detail:
        return response.response(10,"reply_detail not empty .....")

    try:
        if claim_select:
            print("======:::::::")
            sql = "insert into reply (content,claim,user_id,claim_id,time,reply,reply_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (reply_detail,claim_select,response.session_uid(),claim_id,datetime.now(),"",None))
        else:
            sql = "insert into reply (content,reply,user_id,claim_id,reply_id,time,claim) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (reply_detail,reply_select,response.session_uid(),
                                 claim_id,reply_id,datetime.now(),""))
        data = conn.commit()
    except Exception as e:
        print("E: ",e)
        return response.response(6,"insert reply error .")

    return response.response()

@app.route("/replys/<claim_id>")
def replys(claim_id):
    requests = BaseResponseParams(request)

    try:
        sql = "select * from claim inner join user where " \
              "claim.user_id = user.id and claim.id = %s"
        cursor.execute(sql, (claim_id,))
        claim_obj = cursor.fetchone()
    except Exception as e:
        return redirect(url_for("home"))
    claim_obj = response.change_datetime(claim_obj,"time")

    # sql = "select * from claim_relation inner join claim inner join claim as cl2" \
    #       "where claim_relation.claim_id_1 = claim.id and claim_relation.claim_id_1 = %s and cl2.id = claim_relation.claim_id_2"
          #"where claim_relation.claim_id_1 = claim.id and claim.id = %s"
    sql = "select cl2.heading,claim_relation.type,cl2.time from claim_relation inner join claim inner join claim as cl2 where claim_relation.claim_id_1 = claim.id and claim.id = %s and cl2.id = claim_relation.claim_id_2"
    cursor.execute(sql, (claim_id,))
    claim_relations = cursor.fetchall()
    claim_relations = response.change_datetime(claim_relations, "time")

    sql = "select reply.id,reply.content,reply.time," \
          "reply.claim,reply.reply,reply.reply_id," \
          "user.user_name from reply " \
          "inner join claim inner join user " \
          "where reply.claim_id = claim.id and user.id = reply.user_id and reply.claim_id = %s"
    cursor.execute(sql,(claim_id,))
    reply_relations = cursor.fetchall()
    reply_relations = response.change_datetime(reply_relations, "time")

    px = 25
    print("reply_relations: ",reply_relations)
    def get_reply_list(nid=-1,index=0):
        tmp_list = []

        if nid > 0 :
            for rr in reply_relations:
                cur_id = rr["id"]
                reply_id = rr["reply_id"]
                if nid != reply_id:
                    continue
                rr["index"] = f"margin-left: {index * px}px;"
                tmp_list.append(rr)
                tmp_list.extend(get_reply_list(cur_id,index+1))
        else:
            for rr in reply_relations:
                cur_id = rr["id"]
                cur_reply_id = rr["reply_id"]
                if cur_reply_id:
                    continue
                rr["index"] = f"margin-left: {index * px}px;"
                tmp_list.append(rr)
                tmp_list.extend(get_reply_list(cur_id,index+1))
        return tmp_list
    reply_list = get_reply_list()
    print("reply_list: ",reply_list)

    opposed_list = []
    equivalent_list = []
    for cl_obj in claim_relations:
        claim_type = cl_obj["type"]
        if claim_type == "opposed":
            opposed_list.append(cl_obj)
        else:
            equivalent_list.append(cl_obj)
    print("opposed_list: ",opposed_list)
    print("equivalent_list: ",equivalent_list)

    return render_template("replys.html",
                           claim_id = claim_id,
                           claim_obj = claim_obj,
                           claim_relations = claim_relations,
                           opposed_list=opposed_list,
                           equivalent_list=equivalent_list,
                           reply_list=reply_list,
                           )

if __name__ == "__main__":
    app.run(debug=True)