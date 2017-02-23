from django.shortcuts import render, redirect


def index(request):
    return redirect('member:login')