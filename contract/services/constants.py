BASE_CONTRACT = """
<div>
		<p>
			{% if company %} {{company.name}}<br />
			{{company.address}}<br />
			{{company.zip_code}}&nbsp;{{company.city}}<br />
			{% endif %} Tlf: {{customer_contact_phone}}<br />
			E-mail:{{customer_email}}
		</p>

		<p>{{company_image}}</p>

	<p>&nbsp;</p>

	<h1>Kontrakt</h1>

	<table border="0" cellpadding="1" cellspacing="1" style="width:1000px" summary="adsadas">
		<tbody>
			<tr>
				<td><strong>Artister</strong>:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
				<td>{{artist.name}}</td>
			</tr>
			<tr>
				<td>Engasjementets art:</td>
				<td>Artist</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Arrang&oslash;r&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
				<td>{{company.name}}</td>
			</tr>
			<tr>
				<td>Orgnummer:</td>
				<td>{{org_number}}</td>
			</tr>
			<tr>
				<td>Adresse:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</td>
				<td>{{customer.address}}&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>BemyndighetF&oslash;dselsdato:&nbsp;</td>
				<td>{{cust_cont_full_name}}</td>
			</tr>
			<tr>
				<td>kontrahent:</td>
				<td>{{cusomer_date_of_birth}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>E-post:</td>
				<td>{{customer_email}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><strong>Generell informasjon:</strong></td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Datoer:&nbsp; (d.m.y or y-d-m)</td>
				<td><span style="color:#2c3e50">______________________________</span></td>
			</tr>
			<tr>
				<td>Spillested:</td>
				<td>{{venue.name}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Kapasitet:</td>
				<td>{{venue.capacity}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><strong>Honorar:</strong></td>
				<td><strong>NOK</strong> <strong><span style="color:#2c3e50">__________________________</span></strong></td>
			</tr>
			<tr>
				<td>Betaling:</td>
				<td><span style="color:#2c3e50">______________________________</span></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td><span style="color:#2c3e50">______________________________</span></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><em>Annet</em></td>
				<td><span style="color:#2c3e50">______________________________</span></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td><span style="color:#2c3e50">______________________________</span></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td><span style="color:#2c3e50">______________________________</span></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td><span style="color:#2c3e50">______________________________</span></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td><span style="color:#2c3e50">______________________________</span></td>
			</tr>
		</tbody>
	</table>

	<p>&nbsp;</p>

	<p>&nbsp; &nbsp; &nbsp; &nbsp;</p>

</div>
<hr />
<p>&nbsp;</p>
{% if company %}
	<div>

		<h2 style="text-align:center"><strong>{{company.name}} Terms</strong></h2>

		<p>{{company.terms}}</p>

	</div>
<hr />
{% endif %}
<div>

	<h2 style="text-align:center"><strong>{{artist.name}}</strong></h2>

	<h3 style="text-align:center">Hospitality Rider</h3>

	<h4 style="text-align:center">Vedlegg 1 til kontrakt</h4>

	<p>{{artist.hospitality_raider}}</p>
</div>

<hr />
<div>
	<h2 style="text-align:center"><strong>{{artist.name}}</strong></h2>

	<h3 style="text-align:center">Hospitality Rider</h3>

	<h4 style="text-align:center">Vedlegg 1 til kontrakt</h4>

	<p style="text-align:right">{{artist.technical_raider}}</p>

	<p>&nbsp;</p>
</div>
<hr />

"""


EDIT_CONTRACT = """
<div>
	<p>
		<p>
			{% if company %}
			{{company.name}}<br />
			{{company.address}}<br />
			{{company.zip_code}}&nbsp;{{company.city}}<br />
			{% endif %}
			Tlf: {{customer_contact_phone}}<br />
			E-mail:{{customer_email}}
		</p>

		<p>{{company_image}}</p>
	</p>

	<p>&nbsp;</p>

	<h1>Kontrakt</h1>

	<table border="0" cellpadding="1" cellspacing="1" style="width:1000px" summary="adsadas">
		<tbody>
			<tr>
				<td><strong>Artister</strong>:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
				<td>{{artist.name}}</td>
			</tr>
			<tr>
				<td>Engasjementets art:</td>
				<td>Artist</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Arrang&oslash;r&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
				<td>{{company.name}}</td>
			</tr>
			<tr>
				<td>Orgnummer:</td>
				<td>{{org_number}}</td>
			</tr>
			<tr>
				<td>Adresse:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</td>
				<td>{{customer.address}}&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>BemyndighetF&oslash;dselsdato:&nbsp;</td>
				<td>{{cust_cont_full_name}}</td>
			</tr>
			<tr>
				<td>kontrahent:</td>
				<td>{{cusomer_date_of_birth}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>E-post:</td>
				<td>{{customer_email}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><strong>Generell informasjon:</strong></td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Datoer:&nbsp;</td>
				<td><span style="color:#2c3e50">{{contract.date}}</span></td>
			</tr>
			<tr>
				<td>Spillested:</td>
				<td>{{venue.name}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Kapasitet:</td>
				<td>{{venue.capacity}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><strong>Honorar:</strong></td>
				<td><strong>NOK</strong> <span style="color:#2c3e50"><strong>{{contract.price}}</strong></span></td>
			</tr>
			<tr>
				<td>Betaling:</td>
				<td><span style="color:#2c3e50">{{p_methods_one}}</span></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td><span style="color:#2c3e50">{{p_methods_two}}</span></td>
			</tr>
		</tbody>
	</table>

	<p>&nbsp;</p>

	<p><em>Annet&nbsp; &nbsp; &nbsp;<span style="color:#2c3e50">{{comment}}</span></em><br />
	&nbsp; &nbsp; &nbsp; &nbsp;</p>

</div>

<hr />

{% if company %}
<div>
	<h2 style="text-align:center"><strong>{{company.name}} Terms</strong></h2>

	<p>{{company.terms}}</p>

</div>
<hr />
{% endif %}

<div>
	<h2 style="text-align:center"><strong>{{artist.name}}</strong></h2>

	<h3 style="text-align:center">Hospitality Rider</h3>

	<h4 style="text-align:center">Vedlegg 1 til kontrakt</h4>

	<p>{{artist.hospitality_raider}}</p>
</div>

<hr />
<div>
	<h2 style="text-align:center"><strong>{{artist.name}}</strong></h2>

	<h3 style="text-align:center">Hospitality Rider</h3>

	<h4 style="text-align:center">Vedlegg 1 til kontrakt</h4>

	<p style="text-align:right">{{artist.technical_raider}}</p>
</div>
<hr />
<p>&nbsp;</p>

"""

PDF_CONTRACT = """
<div style="position: relative;">
	<p>
		<p>
			{% if company %}
			{{company.name}}<br />
			{{company.address}}<br />
			{{company.zip_code}}&nbsp;{{company.city}}<br />
			{% endif %}
			Tlf: {{customer_contact_phone}}<br />
			E-mail:{{customer_email}}
		</p>

		<p>{{company_image}}</p>
	</p>

	<p>&nbsp;</p>
	<p>&nbsp;</p>
	<h1>Kontrakt</h1>

	<table border="0" cellpadding="1" cellspacing="1" style="width:1000px" summary="adsadas">
		<tbody>
			<tr>
				<td><strong>Artister</strong>:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
				<td>{{artist.name}}</td>
			</tr>
			<tr>
				<td>Engasjementets art:</td>
				<td>Artist</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Arrang&oslash;r&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
				<td>{{company.name}}</td>
			</tr>
			<tr>
				<td>Orgnummer:</td>
				<td>{{org_number}}</td>
			</tr>
			<tr>
				<td>Adresse:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; </td>
				<td>{{customer.address}}&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>BemyndighetF&oslash;dselsdato:&nbsp;</td>
				<td>{{cust_cont_full_name}}</td>
			</tr>
			<tr>
				<td>kontrahent:</td>
				<td>{{cusomer_date_of_birth}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>E-post:</td>
				<td>{{customer_email}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><strong>Generell informasjon:</strong></td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Datoer:&nbsp;</td>
				<td><span style="color:#2c3e50">{{contract.date}}</span></td>
			</tr>
			<tr>
				<td>Spillested:</td>
				<td>{{venue.name}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>Kapasitet:</td>
				<td>{{venue.capacity}}</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><strong>Honorar:</strong></td>
				<td><strong>NOK</strong> <span style="color:#2c3e50"><strong>{{contract.price}}</strong></span></td>
			</tr>
			<tr>
				<td>Betaling:</td>
				<td><span style="color:#2c3e50">{{p_methods_one}}</span></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td><span style="color:#2c3e50">{{p_methods_two}}</span></td>
			</tr>
		</tbody>
	</table>

	<p>&nbsp;</p>
	{% if comment.strip %}
		<p><em>Annet&nbsp; &nbsp; &nbsp;<span style="color:#2c3e50">{{comment}}</span></em><br />
		&nbsp; &nbsp; &nbsp; &nbsp;</p>
	{% endif %}

</div>

{% if company %}
	<div class="company_div" style="position: relative;">
		<p>
			<p style="padding-top:5px">
				{% if company %}
				{{company.name}}<br />
				{{company.address}}<br />
				{{company.zip_code}}&nbsp;{{company.city}}<br />
				{% endif %}
				Tlf: {{customer_contact_phone}}<br />
				E-mail:{{customer_email}}
			</p>

			<p>{{company_image}}</p>
		</p>
		<p>&nbsp;</p>
		<p>&nbsp;</p>
		<h2 style="text-align:center"><strong>{{company.name}} Terms</strong></h2>

		{{company.terms}}

	</div>
{% endif %}

<div style="position: relative; ">
	<p>
		<p style="padding-top:5px">
			{% if company %}
			{{company.name}}<br />
			{{company.address}}<br />
			{{company.zip_code}}&nbsp;{{company.city}}<br />
			{% endif %}
			Tlf: {{customer_contact_phone}}<br />
			E-mail:{{customer_email}}
		</p>

		<p>{{company_image}}</p>
	</p>

	<p>&nbsp;</p>
	<p>&nbsp;</p>	
	<h2 style="text-align:center"><strong>{{artist.name}}</strong></h2>

	<h3 style="text-align:center">Hospitality Rider</h3>

	<h4 style="text-align:center">Vedlegg 1 til kontrakt</h4>

	<p>{{artist.hospitality_raider}}</p>
</div>
<div style="position: relative; margin-top: 5px">
	<p>
		<p style="padding-top:5px">
			{% if company %}
			{{company.name}}<br />
			{{company.address}}<br />
			{{company.zip_code}}&nbsp;{{company.city}}<br />
			{% endif %}
			Tlf: {{customer_contact_phone}}<br />
			E-mail:{{customer_email}}
		</p>

		<p>{{company_image}}</p>
	</p>

	<p>&nbsp;</p>
	<p>&nbsp;</p>
	<h2 style="text-align:center"><strong>{{artist.name}}</strong></h2>

	<h3 style="text-align:center">Technical Rider</h3>

	<h4 style="text-align:center">Vedlegg 1 til kontrakt</h4>

	<p style="text-align:right">{{artist.technical_raider}}</p>
</div>

"""


BASE_FIELD_LENGTH = 30
