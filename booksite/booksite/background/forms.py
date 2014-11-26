# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ValidationError
from booksite.book.models import BookPage, Book
from .models import ReplaceRule


class ReplaceRuleCreateForm(forms.Form):
    rule_res = forms.CharField(label="匹配表达式", max_length=256)
    replace_to = forms.CharField(label="替换为", max_length=256, required=False)

    def save(self):
        if self.is_valid():
            new_rule = ReplaceRule(
                self.cleaned_data['rule_res'].encode('utf-8'),
                self.cleaned_data['replace_to'].encode('utf-8'),
            )
            new_rule.save()
        else:
            raise ValidationError()


class ReplaceBookApplyForm(forms.Form):
    SELECT = (
        ('preview', "预览"),
        ('save', "保存"),
    )
    rule_res = forms.CharField(label="匹配表达式", max_length=256)
    replace_to = forms.CharField(label="替换为", max_length=256, required=False)
    book_id = forms.CharField(label="书籍编号", max_length=10)
    p_or_s = forms.ChoiceField(choices=SELECT, widget=forms.RadioSelect)

    def get_rule(self):
        if self.is_valid():
            return ReplaceRule(
                self.cleaned_data['rule_res'],
                self.cleaned_data['replace_to'],
            )
        else:
            raise ValidationError()

    def get_book(self):
        if self.is_valid():
            return Book.objects.get(pk=self.cleaned_data['book_id'])
        else:
            raise ValidationError()


class ReplacePageApplyForm(forms.Form):
    SELECT = (
        ('preview', "预览"),
        ('save', "保存"),
    )
    rule_res = forms.CharField(label="匹配表达式", max_length=256)
    replace_to = forms.CharField(label="替换为", max_length=256, required=False)
    page_number = forms.CharField(label="章节编号", max_length=10)
    p_or_s = forms.ChoiceField(choices=SELECT, widget=forms.RadioSelect)

    def get_rule(self):
        if self.is_valid():
            return ReplaceRule(
                self.cleaned_data['rule_res'],
                self.cleaned_data['replace_to'],
            )
        else:
            raise ValidationError()

    def get_page(self):
        if self.is_valid():
            return BookPage.objects.get(page_number=self.cleaned_data['page_number'])
        else:
            raise ValidationError()
