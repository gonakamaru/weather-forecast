// Anonymous Apex to empty Recycle Bin

List<Id> ids = new List<Id>();
for (ContentDocument cd : [SELECT Id FROM ContentDocument WHERE IsDeleted = true ALL ROWS]) {
    ids.add(cd.Id);
}

// emptyRecycleBin() throws an error if called with an empty list, so we guard here.
if (!ids.isEmpty()) {
    Database.emptyRecycleBin(ids);
    System.debug(ids.size() + ' record(s) purged from Recycle Bin.');
} else {
    System.debug('Recycle Bin already empty. Nothing to do.');
}