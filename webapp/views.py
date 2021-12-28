from decimal import Decimal
import json
from uuid import UUID, uuid4
import uuid
from django.forms.forms import Form
from django.http import HttpResponse, HttpRequest, response
import os
from django.shortcuts import render
from account.account import Account
from database.database import ObjectNotFound
from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.pandas_db import AccountDatabasePandas, TransactionDatabasePandas
from database.implementations.ram import AccountDatabaseRAM

databaseAccount = AccountDatabasePandas()
databaseTransaction = TransactionDatabasePandas()

def accounts_list(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        accounts = databaseAccount.get_objects()
        maxUS = Decimal(0)
        maxKZ = Decimal(0)
        maxEU = Decimal(0)
        maxTR = Decimal(0)
        max = {
            "USD": uuid,
            "KZT": uuid,
            "TRY": uuid,
            "EUR": uuid,
        }
        for account in accounts:
            if account.currency == 'USD' and account.balance >= maxUS:
                maxUS = account.balance
                max["USD"] = account.id_
            if account.currency == 'KZT' and account.balance >= maxKZ:
                maxKZ = account.balance
                max["KZT"] = account.id_
            if account.currency == 'TRY' and account.balance >= maxTR:
                maxTR = account.balance
                max["TRY"] = account.id_
            if account.currency == 'EUR' and account.balance >= maxEU:
                maxEU = account.balance
                max["EUR"] = account.id_

        print(max)
        return render(request, "index.html", context={'accounts': accounts, 'max':max})

    if request.method == "POST":
        result = request.POST["curChoice"]
        print(result)
        try:
            account = Account.randomwithZ(result)
            try:
                databaseAccount.get_object(account.id_)
                return HttpResponse(content=f"Error: object already exists, use PUT to update", status=400)
            except ObjectNotFound:
                databaseAccount.save(account)
                return HttpResponse(content=account.to_json_str(), status=201)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)

def transaction(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        transactions = databaseTransaction.get_objects()
        return render(request, "transaction.html", context={'transactions': transactions})

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(content="""
    <html>
        <body>
           <h1>Please choose link: </h1> 
           <h3><a href="/accounts/">See accounts information</a></h3>
           <h3><a href="/api/accounts/">See accounts json list</a></h3> 
        </body>
    </html>
    """)

def accounts(request: HttpRequest) -> HttpResponse:
    accounts = databaseAccount.get_objects()

    if request.method == "GET":
        json_obj = [account.to_json() for account in accounts]
        return HttpResponse(content=json.dumps(json_obj))   

    if request.method == "POST":
        try:
            account = Account.from_json_str(request.body.decode("utf8"))
            account.id_ = uuid4()
            try:
                databaseAccount.get_object(account.id_)
                return HttpResponse(content=f"Error: object already exists, use PUT to update", status=400)
            except ObjectNotFound:
                databaseAccount.save(account)
                return HttpResponse(content=account.to_json_str(), status=201)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)

    if request.method == "PUT":
        try:
            account = Account.from_json_str(request.body.decode("utf8"))
            databaseAccount.get_object(account.id_)
            databaseAccount.save(account)
            return HttpResponse(content="OK", status=200)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)
