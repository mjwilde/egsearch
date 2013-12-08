type file;

app (file searchOut) esearch (int numSlices, int sliceNumber)
{
  esearch numSlices sliceNumber @searchOut ;
}

app (file joinOut) join ( string dir, file segment[])
{
  join dir @joinOut 2 ;
}

main()
{
  string outDir  = @arg("dir","/home/slv/lungsearch/out");
  int numSlices  = @toInt(@arg("numSlices","100000"));
  int firstSlice = @toInt(@arg("firstSlice","0"));
  int lastSlice  = @toInt(@arg("lastSlice","1"));

  file segments[];

  foreach s, i in [firstSlice:lastSlice] {
    file f<single_file_mapper; file=@strcat(outDir,"/s.",i,".csv")>;
    f = esearch(numSlices,s);
    segments[i] = f;
  }
  file joined<"esearch.csv">;
}

main();
