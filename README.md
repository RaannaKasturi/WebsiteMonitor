# Website Monitor (Under Development)

### Checkout the Demo App: [https://raannakasturi-websitemonitor.hf.space/](https://raannakasturi-websitemonitor.hf.space/)

### Development Status

- [x] Gets Website Status <sup>[20/06/2024]</sup>
- [x] Gets Website Screenshot <sup>[21/06/2024]</sup>
- [x] Setup auto website checker that checks the website after every few hours (3 Hours) <sup>[23/06/2024]</sup>
- [x] Database connection to store data for long time [Store Webite and User Details] [Store Website Monitor Details] <sup>[25/06/2024]</sup>
- [x] Receieve mails for website down <sup>[25/06/2024]</sup>
- [x] Create a single script which can be used to access all the data & execute entire application:
  - [x] Inputs
    - [x] Email ID
    - [x] URL/domain
  - [x] Outputs
    - [x] Domain
    - [x] URL
    - [x] Code
    - [x] Status
    - [x] WebStatus
    - [x] More Details
    - [x] Screenshot
    - [x] Screenshot URL
    - [x] Email ID
    - [x] Downcount
- [ ] Integrate cronJob
  - [ ] Check all domain after 30 minutes
  - [ ] if domain is inactive/down for more then 10 times check at 1 hour intervals => check at 3 hours interval
  - [ ] if domain is inactive/down for more than 25 times check at 3 hours intervals => check at 6 hours interval
  - [ ] if domain is inactive/down for more than 50 times check at 6 hours intervals => check at 12 hours interval
  - [ ] if domain is inactive/down for more than 75 times check at 12 hours intervals => check at 24 hours interval
  - [ ] if domain is inactive/down for more than 100 times check at 24 hours intervals => delete the domain
- [ ] Shift from Gradio UI to any other, preferably Django or ReactJS<br>
      ...Still Thinking. If you have any Ideas💡, ping me!
