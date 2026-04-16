from flask import Blueprint

# 建立 Blueprint 實例，用以切割路由
task_bp = Blueprint('task_routes', __name__)

@task_bp.route('/')
def index():
    """
    HTTP GET /
    呼叫 Task.get_all() 讀取所有任務清單。
    輸出：渲染 index.html，顯示全部任務清單與新增任務的表單。
    """
    pass

@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """
    HTTP POST /tasks/add
    接收表單傳來的名稱(title)與重要性(priority)等資料，呼叫 Task.create() 存入資料庫。
    輸出：重導向至 '/'。
    若 title 為空，則處理錯誤並導回首頁。
    """
    pass

@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    HTTP POST /tasks/<task_id>/toggle
    更新目標任務是否完成的狀態 (Task.toggle_status)。
    輸出：完成後重導向至 '/'。
    """
    pass

@task_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """
    HTTP GET /tasks/<task_id>/edit:
        呼叫 Task.get_by_id(task_id) 並渲染 edit.html 顯示表單供使用者修改。
    
    HTTP POST /tasks/<task_id>/edit:
        接收表單資料，呼叫 Task.update() 覆蓋寫入該筆紀錄。
        完成後重導向至 '/'。
    """
    pass

@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    HTTP POST /tasks/<task_id>/delete
    呼叫 Task.delete(task_id) 把目標任務從資料庫刪除。
    輸出：完成後重導向至 '/'。
    """
    pass
