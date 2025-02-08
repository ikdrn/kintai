# kintai_back/attendance_app/views.py

import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Employee, Attendance

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        # リクエストボディから JSON をパース
        data = json.loads(request.body)
        emplid = data.get('employeeId')
        if not emplid:
            return JsonResponse({'success': False, 'message': '社員番号が必要です'}, status=400)
        try:
            # 既存の employees テーブルからレコードを取得
            employee = Employee.objects.get(EMPLID=emplid)
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'message': '社員番号が存在しません'}, status=404)
        # セッションにログイン情報を保存
        request.session['employee'] = {
            'EMPLID': employee.EMPLID,
            'EMPLNM': employee.EMPLNM
        }
        return JsonResponse({
            'success': True,
            'employee': {
                'EMPLID': employee.EMPLID,
                'EMPLNM': employee.EMPLNM
            }
        })
    except Exception as e:
        # 詳細なエラー内容をログに出力（開発時のみ）
        print("login_view error:", e)
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    request.session.flush()
    return JsonResponse({'success': True})

@require_http_methods(["GET"])
def get_attendance(request):
    employee_data = request.session.get('employee')
    if not employee_data:
        return JsonResponse({'success': False, 'message': 'ログインしていません'}, status=403)
    emplid = employee_data.get('EMPLID')
    year = request.GET.get('year')
    month = request.GET.get('month')
    if not (year and month):
        return JsonResponse({'success': False, 'message': 'yearとmonthが必要です'}, status=400)
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'yearとmonthは整数で指定してください'}, status=400)
    
    attendances = Attendance.objects.filter(
        ATTEID__EMPLID=emplid,
        ATTEDT__year=year,
        ATTEDT__month=month
    )
    data = []
    for att in attendances:
        data.append({
            'date': att.ATTEDT.strftime('%Y-%m-%d'),
            'startTime': f'{att.ATTEST[:2]}:{att.ATTEST[2:]}',
            'endTime': f'{att.ATTEET[:2]}:{att.ATTEET[2:]}'
        })
    return JsonResponse({'success': True, 'data': data})

@csrf_exempt
@require_http_methods(["POST"])
def update_attendance(request):
    employee_data = request.session.get('employee')
    if not employee_data:
        return JsonResponse({'success': False, 'message': 'ログインしていません'}, status=403)
    emplid = employee_data.get('EMPLID')
    try:
        data = json.loads(request.body)
        date_str = data.get('date')
        start_time = data.get('startTime')
        end_time = data.get('endTime')
        if not (date_str and start_time and end_time):
            return JsonResponse({'success': False, 'message': '必要なパラメータが不足しています'}, status=400)
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            datetime.strptime(start_time, '%H:%M')
            datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return JsonResponse({'success': False, 'message': '日付または時刻の形式が不正です'}, status=400)
        
        start_time_db = start_time.replace(":", "")
        end_time_db = end_time.replace(":", "")
        
        employee = Employee.objects.get(EMPLID=emplid)
        attendance, created = Attendance.objects.update_or_create(
            ATTEID=employee,
            ATTEDT=date_obj,
            defaults={'ATTEST': start_time_db, 'ATTEET': end_time_db}
        )
        return JsonResponse({'success': True, 'created': created})
    except Exception as e:
        print("update_attendance error:", e)
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
