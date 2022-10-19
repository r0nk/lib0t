#!/bin/env python3

import interactions
import shortuuid
import pickle
import os

token = open('token.txt','r').readlines()[0].strip('\n')
lib0t = interactions.Client(token=token)

class Book:
    def __init__(self,name,description,owner):
        self.id=shortuuid.uuid()
        self.name=name
        self.description=description
        self.owner=owner
        self.borrower="NONE"
        self.status="AVAILABLE"
                    #"REQUESTED"
                    #"BORROWED"
    def __repr__(self):
        return str(self.__dict__)

library = []

@lib0t.command(name="add",description="Add a book/object to the library",
        options = [
        interactions.Option(
            name="name",
            description="the name for the object",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="description",
            description="the description for the object",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def add_book(ctx,name:str,description:str):
    owner=ctx.user.username + "#" + ctx.user.discriminator
    b = Book(name,description,owner)
    fOutput = "Added book **\""+b.name+"\"** ["+b.id+"]"
    library.append(b)
    print(f"User {owner} added {b}");
    await ctx.send(fOutput)

@lib0t.command(name="remove",description="Remove a book/object from the library",
        options = [
        interactions.Option(
            name="id",
            description="The id of the book to remove. (/list to view ids)",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def remove_book(ctx,id:str):
    fOutput = "Couldn't find book:" + id
    user = ctx.user.username + "#" + ctx.user.discriminator
    for index, book in enumerate(library):
        if book.id == id:
            if book.owner == user:
                fOutput = "Deleting book " + id
                print(f"User {owner} removed {book}");
                del library[index]
            else:
                fOutput = "Not the owner of " + id
    await ctx.send(fOutput)

@lib0t.command(name="list",description="List all books and their status.")
async def list(ctx):
    fOutput = ":books: Books :books:\n\n"
    for book in library:
        if book.status == "AVAILABLE":
            fOutput += ":green_circle:" + "\t**\"" + book.name + "\"** :crown::" + book.owner + " :id::" + book.id +"\n"
        else:
            fOutput += ":red_circle:" + "\t**\"" + book.name + "\"** :crown::" + book.owner + " :book::" + book.borrower+" :id::" + book.id +"\n"
    await ctx.send(fOutput)

@lib0t.command(name="borrow",description="Borrow a book from the library",
        options = [
        interactions.Option(
            name="id",
            description="the id for the object",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def borrow_book(ctx,id:str):
    user = ctx.user.username + "#" + ctx.user.discriminator
    fOutput = "Couldn't borrow book."
    for index, book in enumerate(library):
        if book.id == id and library[index].status=="AVAILABLE":
            fOutput = "Borrowing **\""+book.name+"\"**"
            library[index].borrower=user
            library[index].status="BORROWED"
            print(f"User {owner} borrowed {book}");
    await ctx.send(fOutput)

@lib0t.command(name="return",description="Return a book to the library",
        options = [
        interactions.Option(
            name="name",
            description="the name for the object",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def return_book(ctx,name:str):
    fOutput = "Couldn't return book."
    user=ctx.user.username + "#" + ctx.user.discriminator
    for index, book in enumerate(library):
        if book.id == id and user == book.borrower:
            fOutput = "Returning **\""+book.name+"\"**"
            library[index].borrower="NONE"
            library[index].status="AVAILABLE"
            print(f"User {owner} returned {book}");
    await ctx.send(fOutput)

lib0t.start()

@lib0t.event
async def on_ready():
    print("The bot is now online.")

