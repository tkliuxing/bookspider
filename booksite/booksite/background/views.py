# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from booksite.book.models import Book, BookPage
from .models import ReplaceRule, FengTui, JingTui
from .forms import (
    ReplaceRuleCreateForm,
    ReplacePageApplyForm,
    ReplaceBookApplyForm,
    TuiJianForm,
)

@permission_required('usercenter.can_add_user')
def index(request):
    C = {}
    CATEGORYS = {
        "a": "侦探推理",
        "b": "武侠修真",
        "c": "网游动漫",
        "d": "历史军事",
        "e": "都市言情",
        "f": "散文诗词",
        "g": "玄幻魔法",
    }.values()
    book_count = Book.objects.all().count()
    category_data = [
        [c, Book.objects.filter(category=c).count()] for c in CATEGORYS
    ]
    C['category_data'] = json.dumps(category_data)
    C['book_count'] = book_count
    return render(request, "background/index.jade", C)

@permission_required('usercenter.can_add_user')
def replace(request):
    C = {}
    form = ReplaceRuleCreateForm()
    if request.method == "POST":
        form = ReplaceRuleCreateForm(request.POST)
        if form.is_valid():
            form.save()
    replace_rule = ReplaceRule.all()
    C['replace_rule'] = replace_rule
    C['create_rule_form'] = form
    return render(request, "background/replace.jade", C)

@permission_required('usercenter.can_add_user')
def edit_rule(request, pk=None):
    C = {}
    rule = ReplaceRule.get(pk)
    form = ReplaceRuleCreateForm({
        'rule_res': rule.rule_res,
        'replace_to': rule.replace_to,
    })
    if request.method == "POST":
        form = ReplaceRuleCreateForm(request.POST)
        if form.is_valid():
            rule.rule_res = form.cleaned_data['rule_res']
            rule.replace_to = form.cleaned_data['replace_to']
            rule.save()
            return redirect('bbg:replace')
    replace_rule = ReplaceRule.all()
    C['replace_rule'] = replace_rule
    C['create_rule_form'] = form
    C['edit_rule'] = True
    return render(request, "background/replace_edit.jade", C)

@permission_required('usercenter.can_add_user')
def delete_rule(request, pk=None):
    rule = ReplaceRule.get(pk)
    rule.delete()
    return redirect(request.META['HTTP_REFERER'])

@permission_required('usercenter.can_add_user')
def apply_rule(request, pk=None):
    C = {}
    rule = ReplaceRule.get(pk)
    C['rule'] = rule
    book_id = request.REQUEST.get('bi', '')
    page_number = request.REQUEST.get('pn', '')
    C['book_id'] = book_id
    C['page_number'] = page_number
    this_is_save = request.method == "POST" and request.POST.get('save', None)
    if not book_id and page_number:
        page = BookPage.objects.get(page_number=page_number)
        if this_is_save:
            page.content = rule.replace(page.content)
            page.save()
        C['save'] = this_is_save
        C['r_content'] = rule.replace(page.content).replace('\n', '\n\n')
        C['content'] = page.content.replace('\n', '\n\n')
        C['page_admin_url'] = "/admin/book/bookpage/%d/" % (page.pk)
        return render(request, "background/replace_apply.jade", C)
    elif book_id:
        book = get_object_or_404(Book, pk=book_id)
        book_pages = BookPage.objects.filter(book_number=book.book_number)
        r_content_list = []
        apply_rule_url = reverse("bbg:apply_rule", args=[pk])
        for page in book_pages:
            if rule.match(page.content):
                page_preview_link = apply_rule_url + "?pn=%s" % page.page_number
                link_a = "<a href='%s' target='_blank'>%s</a>" % (page_preview_link, page.title)
                if this_is_save:
                    page.content = rule.replace(page.content)
                    page.save()
                    r_content_list.append(link_a)
                else:
                    r_content_list.append(link_a)
                    for i in rule.findall(page.content):
                        r_content_list.append(i)
        C['save'] = this_is_save
        C['r_content'] = "\n".join(r_content_list)
        return render(request, "background/replace_apply.jade", C)
    raise Http404

@permission_required('usercenter.can_add_user')
def replace_page(request):
    C = {}
    form = ReplacePageApplyForm(initial=request.REQUEST)
    if request.method == "POST":
        form = ReplacePageApplyForm(request.POST)
        if form.is_valid():
            rule = form.get_rule()
            page = form.get_page()
            if form.cleaned_data['p_or_s'] == 'save':
                page.content = rule.replace(page.content)
                page.save()
                C['save'] = True
            C['r_content'] = rule.replace(page.content).replace('\n', '\n\n')
            C['content'] = page.content.replace('\n', '\n\n')
            C['page_admin_url'] = "/admin/book/bookpage/%d/" % (page.pk)
    C['create_rule_form'] = form
    return render(request, "background/replace_page.jade", C)

@permission_required('usercenter.can_add_user')
def replace_book(request):
    C = {}
    form = ReplaceBookApplyForm(initial=request.REQUEST)
    if request.method == "POST":
        form = ReplaceBookApplyForm(request.POST)
        if form.is_valid():
            rule = form.get_rule()
            book = form.get_book()
            book_pages = BookPage.objects.filter(book_number=book.book_number)
            r_content_list = []
            this_is_save = form.cleaned_data['p_or_s'] == 'save'
            for page in book_pages:
                if rule.match(page.content):
                    page_admin_link = "/admin/book/bookpage/%d/" % (page.pk)
                    link_a = "<a href='%s' target='_blank'>%s</a>" % (page_admin_link, page.title)
                    if this_is_save:
                        page.content = rule.replace(page.content)
                        page.save()
                        r_content_list.append(link_a)
                    else:
                        r_content_list.append(link_a)
                        for i in rule.findall(page.content):
                            r_content_list.append(i)
            C['save'] = this_is_save
            C['r_content'] = "\n".join(r_content_list)
    C['create_rule_form'] = form
    return render(request, "background/replace_book.jade", C)

@permission_required('usercenter.can_add_user')
def tuijian(request):
    C = {}
    C['ft_books'] = FengTui().books or []
    C['jt_books'] = JingTui().books or []
    C['create_ft_form'] = TuiJianForm(model=FengTui)
    C['create_jt_form'] = TuiJianForm(model=JingTui)
    return render(request, 'background/tuijian.jade', C)

@permission_required('usercenter.can_add_user')
def fengtui_create(request):
    C = {}
    if request.method == "POST":
        form = TuiJianForm(model=FengTui, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("bbg:tuijian")
        else:
            C['ft_books'] = FengTui().books
            C['jt_books'] = JingTui().books
            C['create_jt_form'] = TuiJianForm(model=JingTui)
            C['create_ft_form'] = form
            return render(request, 'background/tuijian.jade', C)
    else:
        return redirect("bbg:tuijian")

@permission_required('usercenter.can_add_user')
def jingtui_create(request):
    C = {}
    if request.method == "POST":
        form = TuiJianForm(model=JingTui, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("bbg:tuijian")
        else:
            C['ft_books'] = FengTui().books
            C['jt_books'] = JingTui().books
            C['create_jt_form'] = form
            C['create_ft_form'] = TuiJianForm(model=FengTui)
            return render(request, 'background/tuijian.jade', C)
    else:
        return redirect("bbg:tuijian")

@permission_required('usercenter.can_add_user')
def del_tuijian(request, model='ft', book_id=0):
    if model not in ['ft','jt'] and not Book.objects.filter(id=book_id):
        return redirect("bbg:tuijian")
    book = Book.objects.get(id=book_id)
    if model == 'ft':
        ft = FengTui()
        ft.remove(book)
        ft.save()
    if model == 'jt':
        jt = JingTui()
        jt.remove(book)
        jt.save()
    return redirect("bbg:tuijian")





