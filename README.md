# bioInfo
## Integracija rezultata različitih programa za sklapanje genoma

### Značaj teme i oblasti:

Poznavanje genoma različitih organizama u velikoj meri unapređuje razumevanje živog sveta na Zemlji. Sekvenca DNK je sa računarske strane posmatrano niska nad azbukom  {A,C,G,T}   koja predstavlja niz nukleotida od kojih je sačinjen jedan lanac molekula DNK. Tehnologijom sekvenciranja nove generacije   (NGS)    pomoću specijalizovanih mašina očitavaju se kratki delovi sekvence, koji se zatim povezuju da bi se celokupna DNK sekvenca programski rekonstruisala.   NGS   proizvodi veliki broj kratkih očitavanja koje pokrivaju svaki pojedinačni DNK segment i od izuzetnog je značaja da programi za njihovo povezivanje budu efikasni i da obezbede odgovarajuću tačnost. S obzirom da dužine DNK sekvenci mogu iznositi i nekoliko milijardi baznih parova i da je   NGS tehnologija još uvek neprecizna, kao i da su očitavanja višestruko redundantna, problem sklapanja genoma je računarski veoma kompleksan.

### Specifični cilj rada:

Danas je u upotrebi na desetine programa za sklapanje genoma, asemblera, koji su često zasnovani na De Bruinovim grafovima. Cilj ovog master rada je integracija rezultata različitih asemblera radi dobijanja što kvalitetnije rekonstrukcije DNK sekvence. Praktični deo rada uključuje konfigurisanje alata za integraciju   GAM NGS[1]   koji će biti prilagođen odabranim asemblerima:   Velvet[2]   i    Abyss[3].    Performanse kombinovanog asemblera biće upoređene sa pojedinačnim alatima. Testiranje će se izvesti na sirovim podacima preuzetim iz repozitorijuma sekvenci   SRA[4]   i rezultati će biti upoređeni sa odgovarajućim referentnim genomom. Za prikaz rezultata biće implementirana grafička reprezentacija. Aplikacija će biti razvijena upotrebom programskog jezika   Python. 

### Reference:
1. Vicedomini, Riccardo, et al. "GAM-NGS: genomic assemblies merger for next generation sequencing." BMC bioinformatics 14.7 (2013): S6. 
2. Zerbino, Daniel R., and Ewan Birney. "Velvet: algorithms for de novo short read assembly using de Bruijn graphs." Genome research 18.5 (2008): 821-829. 
3. Simpson, Jared T., et al. "ABySS: a parallel assembler for short read sequence data." Genome research 19.6 (2009): 1117-1123. 	
4. https://www.ncbi.nlm.nih.gov/sra/
