// Anonymous Apex to Empty Recycle Bin

List<Id> ids = new List<Id>();
for (ContentDocument cd : [SELECT Id FROM ContentDocument WHERE IsDeleted = true ALL ROWS]) {
    ids.add(cd.Id);
}

if (!ids.isEmpty()) {
    Database.emptyRecycleBin(ids);
    System.debug('Purged: ' + ids.size() + ' record(s).');
} else {
    System.debug('Recycle Bin already empty. Nothing to do.');
}