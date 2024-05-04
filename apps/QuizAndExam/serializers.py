from rest_framework import serializers
from QuizAndExam.models import Quiz, QuizAnswerSheet, QuizAnswerRecord, Questions, ExamAnswerRecord, Exam, \
    ExamAnswerSheet, QuestionsPicture

class QuestionsPictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionsPicture
        fields = '__all__'
class QuestionsSerializer(serializers.ModelSerializer):
    question_picture =QuestionsPictureSerializer(many=True)
    class Meta:
        model = Questions
        fields = '__all__'

class QuizAnswerRecordSerializer(serializers.ModelSerializer):
    question=QuestionsSerializer(many=False)
    class Meta:
        model = QuizAnswerRecord
        fields = '__all__'
class ExamAnswerRecordSerializer(serializers.ModelSerializer):
    question=QuestionsSerializer(many=False)
    class Meta:
        model = ExamAnswerRecord
        fields = '__all__'

class QuizAnswerRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswerRecord
        fields = ['stu_answer','score','quiz_answer_sheet','question']
class ExamAnswerRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAnswerRecord
        fields = ['stu_answer','score','exam_answer_sheet','question']

class QuizListSerializer(serializers.ModelSerializer):
    # 作业列表序列化
    class Meta:
        model = Quiz
        fields = '__all__'
class ExamListSerializer(serializers.ModelSerializer):
    # 考试列表序列化
    class Meta:
        model = Exam
        fields = '__all__'

class QuizDetailSerializer(serializers.ModelSerializer):
    # 作业详情序列化，请求作业详情时覆盖问题外键字段
    questions=QuestionsSerializer(many=True)
    class Meta:
        model = Quiz
        fields = '__all__'
class ExamDetailSerializer(serializers.ModelSerializer):
    # Exam详情序列化，请求Exam详情时覆盖问题外键字段
    questions=QuestionsSerializer(many=True)
    class Meta:
        model = Exam
        fields = '__all__'

class QuizAnswerSheetListSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    quiz=QuizListSerializer(many=False)
    quiz_answer_record = QuizAnswerRecordSerializer(many=True)
    class Meta:
        model = QuizAnswerSheet
        fields = [ "quiz_answer_record","student","quiz",'teacher']
class ExamAnswerSheetListSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    exam=ExamListSerializer(many=False)
    exam_answer_record = ExamAnswerRecordSerializer(many=True)
    class Meta:
        model = ExamAnswerSheet
        fields = [ "exam_answer_record","student","exam",'teacher']

class QuizAnswerRecordSerializer1(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswerRecord
        fields = ['stu_answer','score','question']
class QuizAnswerSheetCreateSerializer(serializers.ModelSerializer):
    quiz_answer_record = QuizAnswerRecordSerializer1(required=False,many=True)
    class Meta:
        model = QuizAnswerSheet
        fields = [ "quiz_answer_record","quiz"]
    def create(self, validated_data):
        record_set = validated_data.pop('quiz_answer_record')
        quiz_answer_sheet = QuizAnswerSheet.objects.create(**validated_data)
        stu=validated_data.get('student')
        for record_data in record_set:
            QuizAnswerRecord.objects.create(quiz_answer_sheet=quiz_answer_sheet,
                                            student=stu,**record_data)
        return quiz_answer_sheet

class ExamAnswerRecordSerializer1(serializers.ModelSerializer):
    class Meta:
        model = ExamAnswerRecord
        fields = ['stu_answer','score','question']
class ExamAnswerSheetCreateSerializer(serializers.ModelSerializer):
    exam_answer_record = ExamAnswerRecordSerializer1(required=False,many=True)
    class Meta:
        model = ExamAnswerSheet
        fields = [ "exam_answer_record","exam"]
    def create(self, validated_data):
        record_set = validated_data.pop('exam_answer_record')
        exam_answer_sheet = ExamAnswerSheet.objects.create(**validated_data)
        stu=validated_data.get('student')
        for record_data in record_set:
            ExamAnswerRecord.objects.create(exam_answer_sheet=exam_answer_sheet,
                                            student=stu,**record_data)
        return exam_answer_sheet

