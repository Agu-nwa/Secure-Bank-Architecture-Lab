
const output = document.getElementById("api-output");
async function simulatePrivateApi(endpoint){
  if(!output) return;
  output.textContent = "Calling private service simulation: " + endpoint + " ...";
  const demo = {
    "/api/auth/session": { service:"auth-service", privateSubnet:true, status:"session-valid", mfa:"enabled" },
    "/api/accounts/summary": { service:"account-service", privateSubnet:true, balance:"demo-only", source:"private account API" },
    "/api/transfers/risk-check": { service:"transfer-service + fraud-risk-service", privateSubnet:true, decision:"review-required", amount:"demo" },
    "/api/notifications/send": { service:"notification-service", privateSubnet:true, channel:"email/sms queue", status:"queued" },
    "/api/reports/daily": { service:"reporting-service", privateSubnet:true, report:"daily operations summary" }
  };
  setTimeout(()=>{ output.textContent = JSON.stringify(demo[endpoint] || {error:"unknown endpoint"}, null, 2); }, 450);
}
document.addEventListener("DOMContentLoaded",()=>{
  const first=document.querySelector("[data-endpoint]");
  if(first) simulatePrivateApi(first.dataset.endpoint);
});
