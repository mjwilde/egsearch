type file;

app (file searchOut, file out) esearch (file wrapper, file pyscript, int numSlices, int sliceNumber, file inp1, file inp2)
{
    bash @wrapper @pyscript numSlices sliceNumber @searchOut stdout=@out;
}

app (file joinOut) join ( string dir, file segment[])
{
  join dir @joinOut 2 ;
}

main()
{
  string outDir  = @arg("dir","./out");
  int numSlices  = @toInt(@arg("numSlices","100000"));
  int firstSlice = @toInt(@arg("firstSlice","0"));
  int lastSlice  = @toInt(@arg("lastSlice","1"));
  file dict        <"./HG-U133A_2.na33.annot.csv">;
  file results     <"./Consortium_expr_full_pheno_no_affx.csv">;
  file pyscript    <"./exsearch.py">;
  file wrapper     <"./wrapper.sh">;
  file segments[];

  foreach s, i in [firstSlice:lastSlice] {
    file f<single_file_mapper; file=@strcat(outDir,"/s.",i,".csv")>;
    file o<single_file_mapper; file=@strcat(outDir,"/s.",i,".out")>;
    (f,o) = esearch(wrapper, pyscript, numSlices, s, dict, results);
    segments[i] = f;
  }
}

main();
