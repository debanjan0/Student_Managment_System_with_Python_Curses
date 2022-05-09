
<html>
<body>
  <p>
    Table "student_data" {
  "sid" int [pk, not null]
  "name" char(20) [default: NULL]
  "dob" date [default: NULL]
  "phone" int [default: NULL]
  "city" char(15) [default: NULL]
  "class" int [default: NULL]
}

Table "student_marks" {
  "tid" int [pk, not null]
  "sid" int [default: NULL]
  "pyear" int [default: NULL]
  "class" int [default: NULL]
  "sroll" int [default: NULL]
  "tmarks" int [default: NULL]
}


Table "fees" {
  "txid" int [pk, not null, increment]
  "amount" int [default: NULL]
  "pay_date" date [default: NULL]
  "MoP" char(50) [default: NULL]
  "sid" int [ref: > student_data.sid]
}
  </p>
  <img src=https://github.com/debanjan0/Student_Managment_System_with_Python_Curses/blob/main/stu_man_sys.png>
</body>
</html>


