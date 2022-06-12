# etroc-controller

Setup
```
git clone git@github.com:CMS-MTD/etroc-controller.git
```

```
./scanThresholds.py --Qinj 0xFF --outfile data_Qinj_FF_pix1_testing.root
./scanThresholds.py --Qinj 0xCF --outfile data_Qinj_CF_pix1_testing.root
./scanThresholds.py --Qinj 0x87 --outfile data_Qinj_87_pix1_testing.root
./scanThresholds.py --Qinj 0x37 --outfile data_Qinj_37_pix1_testing.root

./makeNtupleHistograms.py --infile data_Qinj_FF_pix1_testing.root
./makeNtupleHistograms.py --infile data_Qinj_CF_pix1_testing.root
./makeNtupleHistograms.py --infile data_Qinj_87_pix1_testing.root
./makeNtupleHistograms.py --infile data_Qinj_37_pix1_testing.root
```

