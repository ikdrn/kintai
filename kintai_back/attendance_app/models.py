# kintai_back/attendance_app/models.py

from django.db import models

class Employee(models.Model):
    EMPLID = models.CharField(max_length=5, primary_key=True)  # 社員番号
    EMPLNM = models.CharField(max_length=100)  # 社員名

    def __str__(self):
        return f'{self.EMPLNM} ({self.EMPLID})'

    class Meta:
        db_table = 'employees'  # 既存のテーブル名に合わせる
        managed = False         # Django にテーブル管理をさせない


class Attendance(models.Model):
    ATTEID = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='ATTEID')  # 外部キー
    ATTEDT = models.DateField()  # 日付
    ATTEST = models.CharField(max_length=4)  # 就業時間 (例: "0900")
    ATTEET = models.CharField(max_length=4)  # 終了時間 (例: "1800")

    class Meta:
        db_table = 'attendance'  # 既存のテーブル名に合わせる
        managed = False         # Django にテーブル管理をさせない
        unique_together = ('ATTEID', 'ATTEDT')  # １日１レコード

    def __str__(self):
        return f'{self.ATTEID} - {self.ATTEDT}'
