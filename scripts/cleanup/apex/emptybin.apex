// Empty Recycle Bin

List<Id> ids = new List<Id>();

for (ContentDocument cd : [SELECT Id FROM ContentDocument WHERE IsDeleted = true ALL ROWS]) {
    ids.add(cd.Id);
}

Database.emptyRecycleBin(ids);