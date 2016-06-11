import json

from rest_framework import serializers

from .models import *

class TestSerializer(serializers.ModelSerializer):
	acl_edit = serializers.SerializerMethodField('can_edit')
	problem = serializers.SerializerMethodField()
	score = serializers.SerializerMethodField('get_user_score')
	finished = serializers.SerializerMethodField('get_user_finished')
	start = serializers.DateTimeField('')

	def can_edit(self, object):
		return self.context['request'].user.has_perm('problems.change_test')

	def get_problem(self, object):
		return object.problem_set.count()

	def get_user_score(self, object):
		if not self.context['request'].user.is_authenticated():
			return None

		return 1

	def get_user_finished(self, object):
		if not self.context['request'].user.is_authenticated():
			return None

		return 1

	class Meta:
		model = Test
		fields = (
			'id', 'name', 'mode', 'start', 'end', 'readonly', 'acl_edit',
			'problem', 'score', 'finished',
		)

class ProblemSerializer(serializers.ModelSerializer):
	acl_edit = serializers.SerializerMethodField('can_edit')
	graders = serializers.SerializerMethodField()
	passed = serializers.SerializerMethodField('get_user_passed')
	test_id = serializers.PrimaryKeyRelatedField(source='test', queryset=Test.objects.all())

	def can_edit(self, object):
		return self.context['request'].user.has_perm('problems.change_problem')

	def get_user_passed(self, object):
		if not self.context['request'].user.is_authenticated():
			return None

		return False

	def get_graders(self, object):
		try:
			data = json.loads(object.graders)
		except json.decoder.JSONDecodeError:
			data = {}

		if type(data) != dict:
			data = {}

		if not object.input or (not object.output and object.comparator == 'hash'):
			data['invalid'] = True

			if not self.can_edit(object):
				for key in ('codejam', 'grader'):
					try:
						del data['key']
					except KeyError:
						pass

		return data

	class Meta:
		model = Problem
		fields = (
			'id', 'name', 'description', 'point', 'creator', 'graders',
			'test_id', 'acl_edit', 'input_lang', 'output_lang', 'comparator',
			'passed',
		)
