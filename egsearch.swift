type file;

app (file searchOut) esearch (int numSlices, int sliceNumber)
{
  # es04-02.py 100000 $s run1
  esearch numSlices sliceNumber @searchOut ;
}

app (file joinOut) join ( string dir, file segment[])
{
  # join.py run1 joined.csv 2
  join dir @joinOut 2 ;
}

main()
{
  string outDir  = @arg("dir","/scratch/midway/wilde/esearch/out");
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
  # joined = join(outDir, segments);
}

main();
