import streamlit as st
import dns.resolver

def extract_domain(user_email):
  if '@' in user_email:
    return user_email.split("@")[-1].strip()
  return user_email.strip()

def get_mail_servers(domain):
  try:
    answers = dns.resolver.resolve(domain, 'MX')
    mail_servers = sorted([(r.preference, r.exchange.to_text()) for r in answers])
    return mail_servers
  except dns.resolver.NoAnswer:
    return "No MX record found"
  except dns.resolver.NXDOMAIN:
    return "Domain does not exist"
  except dns.exception.DNSException as e:
    return f"DNS query failed: {e}"
  
st.title("Email Provider Checker")

user_email = st.text_input("Enter Email Address")

if st.button("Check Email Provider"):

  if user_email:
    user_list = [extract_domain(item.strip()) for item in user_email.split(",") if item.strip()]
    results = {}

    for domain in user_list:
      if "." in domain:
        mx_records = get_mail_servers(domain)
        if isinstance(mx_records, list):
          for pref, exchange in mx_records:
            mx_host = exchange.lower()
            if mx_host.endswith("google.com") or mx_host.endswith("googlemail.com"):
                results[domain] = "Google (Gmail)"
                break
            elif mx_host.endswith("outlook.com") or mx_host.endswith("hotmail.com") or mx_host.endswith("office365.com"):
                results[domain] = "Microsoft (Outlook/Office 365)"
                break
            elif mx_host.endswith("icloud.com") or mx_host.endswith("apple.com"):
                results[domain] = "Apple (iCloud)"
                break
            else:
                results[domain] = f"Other / Filtering System ({exchange})"
        else:
          results[domain] = mx_records
      else:
        results[domain] = "Invalid domain"

    for domain, result in results.items():
      if "Google" in result or "Microsoft" in result or "Apple" in result:
          st.success(f"{domain}: {result}")
      elif "Other" in result:
          st.info(f"{domain}: {result}")
      else:
          st.error(f"{domain}: {result}")
  else:
    st.error("Please enter at least one domain or email address.")
