#!/usr/bin/env python3
import os, json, re

'''
Program to extract the data from the PEN registry and write out a new database
'''

InJSONFileName = "PENwholeJSON.txt"
if not(os.path.exists(InJSONFileName)):
	exit("Could not find {}. Exiting.".format(InJSONFileName))

InJSONFile = open(InJSONFileName, mode="r")
AllRecords = json.load(InJSONFile, encoding="utf-8")

# PEN, Request_ID, Time_Created, Time_Modified, Company_Name, Contact_Name, Contact_Email

PENDict = {}
CompanyList = []
ContactList = []
for ThisRecord in AllRecords:
	# Sanity check on length
	if len(ThisRecord) != 7:
		exit("Found a bad record '{}'. Exiting.".format(ThisRecord))
	# Sanity check on duplicate PENs
	if PENDict.get(ThisRecord[0]) != None:
		exit("Found a duplicate PEN: {}. Exiting.".format(ThisRecord[0]))
	# Some of the records have None instead of "", so fix this
	PENDict[ThisRecord[0]] = ThisRecord[4] if ThisRecord[4] else ""
	CompanyList.append((ThisRecord[4] if ThisRecord[4] else "", ThisRecord[0]))
	ContactList.append((ThisRecord[5] if ThisRecord[5] else "", ThisRecord[0]))

# Report gaps in the PEN list
print("Gaps between PENs:")
PrevPEN = -1
for ThisPEN in sorted(PENDict):
	if ThisPEN - 1 != PrevPEN:
		print("   {} and {}".format(PrevPEN, ThisPEN))
	PrevPEN = ThisPEN

# Report on duplicate companies
NonASCIICompany = []
DupList = []
PrevCompanyTuple = ("", -1)
for ThisCompanyTuple in sorted(CompanyList):
	if ThisCompanyTuple[0] in ("Unassigned", "Reserved", ""):
		continue
	if ThisCompanyTuple[0] == PrevCompanyTuple[0]:
		DupList.append((ThisCompanyTuple[0],ThisCompanyTuple[1]))
		# print("   {} is PEN {} and {}".format(ThisCompanyTuple[0], PrevCompanyTuple[1], ThisCompanyTuple[1]))
	PrevCompanyTuple = ThisCompanyTuple
	try:
		(ThisCompanyTuple[0]).encode('ascii')
	except:
		NonASCIICompany.append(ThisCompanyTuple[0])
print("\nThere were {} duplicate company names.".format(len(DupList)))

# Report on Non-ASCII
NonASCIIContact = []
for ThisContactTuple in ContactList:
	try:
		(ThisContactTuple[0]).encode('ascii')
	except:
		NonASCIIContact.append(ThisContactTuple[0])

print("\nThere were {} non-ASCII company names and {} non-ASCII contact names.".format(len(NonASCIICompany), len(NonASCIIContact)))

NonASCIILetters = {}
BiggerList = NonASCIIContact
BiggerList.extend(NonASCIICompany)
for ThisName in BiggerList:
	for ThisChar in ThisName:
		if ord(ThisChar) > 127:
			NonASCIILetters[ThisChar] = ""

print("The non-ASCII characters are\n{}\n{}".format("".join(sorted(NonASCIILetters)), [ord(x) for x in sorted(NonASCIILetters)]))

# print("\n\nThe non-ASCII company names are:\n{}".format("\n".join(NonASCIICompany)))

