FLAG='sBTSCTF<M0N3Y-I$-HIDDEN-1NSI0E-THE-4M1GA>s'
cp base_save SECRET.S00
echo "$FLAG" | python3 enc.py >> SECRET.S00
echo -e '\r[A#TN*4A' >> SECRET.S00
c1541 -format "passdisk,2" d64 disk.d64
c1541 -attach disk.d64 -write CODE.P00 decrypt
c1541 -attach disk.d64 -write SECRET.S00 secret,s

