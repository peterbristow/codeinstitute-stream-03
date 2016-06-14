#!/usr/bin/env bash
 curl -H "Content-Type: application/json" -X POST -d
 {
  "object":
    {
        "id": "in_18DGVFFYWmpZDF7IhaAM0brx",
        "object": "invoice",
        "amount_due": 1099,
        "application_fee": null,
        "attempt_count": 1,
        "attempted": true,
        "charge": "ch_18DGVFFYWmpZDF7IA5s5lQns",
        "closed": true,
        "currency": "gbp",
        "customer": "cus_8UEzAXAp84DFVv",
        "date": 1463761773,
        "description": null,
        "discount": null,
        "ending_balance": 0,
        "forgiven": false,
        "lines":
        {
            "object": "list",
             "data":[
                {
                    "id": "sub_8UEzAtkQS8HQMJ",
                    "object": "line_item",
                     "amount": 1099,
                    "currency": "gbp",
                    "description": null,
                    "discountable": true,
                    "livemode": false,
                    "metadata": {},
                    "period": {
                        "start": 1463761773,
                        "end": 1466440173
                    },
                    "plan": {
                        "id": "REG_MONTHLY2",
                        "object": "plan",
                        "amount": 1099,
                        "created": 1463751631,
                        "currency": "gbp",
                        "interval": "month",
                        "interval_count": 1,
                        "livemode": false,
                        "metadata": {},
                        "name": "Monthly Subscriptions2",
                        "statement_descriptor": "Monthly Subscription2",
 			"trial_period_days": null
                    },
                    "proration": false,
                    "quantity": 1,
                    "subscription": null,
                    "type": "subscription"
                }
            ]
            "has_more": false,
            "total_count": 1,
            "url": "/v1/invoices/in_18DGVFFYWmpZDF7IhaAM0brx/lines"
         }
        "livemode": false,
        "metadata":{
        },
        "next_payment_attempt": null,
        "paid": true,
        "period_end": 1463761773,
        "period_start": 1463761773,
        "receipt_number": null,
        "starting_balance": 0,
        "statement_descriptor": null,
        "subscription": "sub_8UEzAtkQS8HQMJ",
        "subtotal": 1099,
        "tax": null,
        "tax_percent": null,
        "total": 1099,
        "webhooks_delivered_at": null
    }
}
http://localhost:8000/subscriptions_webhook/
