# ------------------------------------------------------------------
# Python 3+ only!!!
# ------------------------------------------------------------------
import os
import hashlib
import locale

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'


# ------------------------------------------------------------------
# Recull informació dels fitxers en un diccionary indexat per tamany
# ------------------------------------------------------------------
def GetFilesInfo(folderList):

  counter = 0
  filesDict = {} 
  for folder in folderList:
    folder = os.path.expanduser(folder) 
    for path, subdirs, files in os.walk(folder): # També els subdirectoris
      for name in files:
        counter += 1
        filename = os.path.join(path, name)
        filesize = os.stat(filename).st_size
        filesDict.setdefault(filesize,[]).append(filename)
  
  return (filesDict, counter)

# ------------------------------------------------------------------



# ------------------------------------------------------------------
# Calcula el MD5 d'un fitxer i el guarda per no recalcular-lo
# ------------------------------------------------------------------
g_hashDict = {}
def CalculateOrRecoverHash(file):

  global g_hashDict

  if file in g_hashDict:
    md5 = g_hashDict[file]
  else:  
    md5 = hashlib.md5(open(file,'rb').read()).hexdigest()
    g_hashDict[file] = md5  

  return md5

# ------------------------------------------------------------------



# ------------------------------------------------------------------
# Cerca els source_files dins de back_files (segons tamany)
# Opcionalment llegeix i compara el seu contingut (calculant el seu hash MD5).
# ------------------------------------------------------------------
def VerifyBackup(source_files, backup_files, readContent=True, Verbose=True):
  
  missing = []

  # Pas 1 de 2 (fitxers que medeixen el mateix queden pending)
  pending = []
  for size in source_files:
    if size not in backup_files:
      for file in source_files[size]:
        missing.append(file)
    else:
      pending.append(size)

  # Pas 2 de 2 (calcular MD5 dels fitxers que medeixen el mateix)
  if readContent:
    counter = 0
    for size in pending:
      for src_file in source_files[size]:
        found = False
        counter += 1
        if Verbose: print(f"\nSource: {src_file}", flush=True) 
        else: print(f"{counter} \r", end="", flush=True) 
        src_md5 = CalculateOrRecoverHash(src_file)
        for bak_file in backup_files[size]:
          bak_md5 = CalculateOrRecoverHash(bak_file) 
          if src_md5 == bak_md5: 
            if Verbose: print(f">>Backup: {bak_file}", flush=True)
            found = True
        if not found:
          missing.append(src_file)

  print(f"\n{counter} files verified with MD5 hash.")
  if not missing:
    print("No missing files in backup!!!")
  else:  
    print("Missing files in backup:")
    for file in missing:
      print(file)

  return 
# ------------------------------------------------------------------

        

source = ["C:\\MY_DATA"] # Llista de directoris ("C:\\MY_DATA" o "/home/jsmith/") 
backup = ["G:"] # Llista de directoris
source_files, source_counter = GetFilesInfo(source)
backup_files, backup_counter = GetFilesInfo(backup)
print(f"{source_counter} source files in {source}.")
print(f"{backup_counter} backup files in {backup}.")
VerifyBackup(source_files, backup_files, readContent=True, Verbose=False) # readContent es lent però segur!!!


