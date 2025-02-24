#!/usr/bin/env python3

import logging

from django import forms
from django.core.exceptions import ValidationError

from . import models

UUID_LAST_DIGITS = 12


class ProposalForm(forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = [
            "name",
            "surname",
            "email",
            "title",
            "description",
        ]

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {
                "id": "cfp-name",
                "size": "20",
                "placeholder": "Tu nombre",
                "class": "input is-rounded",
            }
        )
        self.fields["surname"].widget.attrs.update(
            {
                "id": "cfp-surname",
                "size": "40",
                "placeholder": "Tus apellidos",
                "class": "input is-rounded",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "id": "cfp-email",
                "size": "40",
                "placeholder": "Tu email",
                "class": "input is-rounded",
            }
        )
        self.fields["title"].widget.attrs.update(
            {
                "id": "cfp-title",
                "size": "60",
                "placeholder": "El título de tu maravillosa charla",
                "class": "input is-rounded",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "id": "cfp-title",
                "cols": "60",
                "rows": "20",
                "placeholder": ("El texto de tu maravillosa charla. "
                                "¿Aceptamos markdown? ¡Por supuesto!"),
                "class": "textarea",
            }
        )
        self.event = event

    def save(self):
        proposal = super().save(commit=False)
        proposal.event = self.event
        proposal.save()
        return proposal


class EmailForm(forms.Form):
    email = forms.EmailField(label="Tu email", max_length=192)


class WaitingListForm(forms.Form):

    email = forms.EmailField(label="Tu email", max_length=192)
    name = forms.CharField(label="Nombre", max_length=256)
    surname = forms.CharField(label="Apellidos", max_length=256)
    phone = forms.CharField(label="Teléfono", max_length=32)

    def __init__(self, event, *args, **kwargs):
        self.event = event
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        assert self.is_valid()
        wl = models.WaitingList(
            event=self.event,
            name=self.cleaned_data["name"],
            surname=self.cleaned_data["surname"],
            email=self.cleaned_data["email"],
            phone=self.cleaned_data["phone"],
            )
        if commit:
            wl.save()
        return wl


class RefundForm(forms.Form):
    email = forms.EmailField(label="Tu email", max_length=192)
    uuid = forms.CharField()

    def __init__(self, event, *args, **kwargs):
        logging.error("Llamada al metodo __init__ de RefundForm")
        super().__init__(*args, **kwargs)
        self.event = event

    def clean_uuid(self):
        email = self.cleaned_data["email"]
        uuid = self.cleaned_data["uuid"]
        if uuid == "tu puta madre":
            raise ValidationError("Cuida ese vocabulario")

        if len(uuid) < UUID_LAST_DIGITS:
            raise ValidationError(
                f"Necesito los últimos {UUID_LAST_DIGITS} letras o dígitos "
                "del código"
                )
        uuid = uuid[-UUID_LAST_DIGITS:]
        tickets = list(
            self.event.all_tickets()
            .filter(customer_email=email)
            .filter(keycode__iendswith=uuid)
        )
        if len(tickets) != 1:
            raise ValidationError(
                "El correo o las últimos {} letras o dígitos del"
                " codigo están mal.".format(UUID_LAST_DIGITS)
            )
        self.ticket = tickets[0]
        if models.Refund.exists(self.event, self.ticket):
            raise ValidationError(
                "Ya se ha solicitado una devolución del importe para ese ticket"
            )
        return uuid
