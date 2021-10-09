from pathlib import Path
from django.utils import timezone
from app.models import *

def generate_invoice_mails(output_dir):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    unpaid_invoices = ToMemberInvoice.objects.filter(payed=False)
    for invoice in unpaid_invoices:
        if not invoice.items.exists():
            invoice.payed = True
            invoice.save()
            continue
            
        person = invoice.items.first().person
        if not person.email:
            print("Person", person.name, "does not have an email. Can't generate invoice")
            continue
            
        if not person.phone:
            print("Person", person.name, "does not have a phone number. Can't generate invoice")
            continue
            
        # we should not send invoices to eta
        if person.is_eta:
            invoice.payed = True
            invoice.save()
            continue

        invoice.sent = True
        invoice.save()
        
        total_cost = sum(map(lambda x: x.cost, invoice.items.all()))
        html = f"<p>Hej {person.name}!</p>" 
        html += "<p>Du har en obetald faktura till ETA!</p>"
        html += f"<p>Totalbelopp: <b>{round(total_cost, 2)}</b> kr</p>"
        html += "<p>Betalas till bankgiro: <b>5930-5680</b></p>"
        html += f"<p>Märk betalningen med <b>{invoice.id}</b></p>"
        html += "<p>Nedan följer en sammanställning av artiklarna utgör fakturan.</p>"
        html += "<table>"
        html += "<tr>"
        html += f"<th>Order date</th>"
        html += f"<th>Item number</th>"
        html += f"<th>Item description</th>"
        html += f"<th>Item count</th>"
        html += f"<th>Total item cost</th>"
        html += "</tr>"
        
        for item in invoice.items.all():
            html += "<tr>"
            html += f"<td>{item.order_placed_at.strftime('%Y-%m-%d')}</td>"
            html += f"<td>{item.item_no}</td>"
            html += f"<td>{item.item_desc}</td>"
            html += f"<td>{item.item_count}</td>"
            html += f"<td>{item.cost:.3f}</td>"
            html += "</tr>"
        
        html += "</table>"
        html += f"<p>Detta mail ska till {person.email}. Går det dåligt ring till {person.phone}.</p>"
        
        file_name = f"{'ETA_' if person.is_eta else ''}{invoice.id}.html"

        filepath = output / file_name
        with filepath.open("w", encoding ="utf-8") as f:
            f.write(html)

        