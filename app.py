from flask import Flask, render_template, request, redirect, url_for, flash
from wakeonlan import send_magic_packet
import yaml
import os

APP_SECRET = os.environ.get("APP_SECRET", "change-me")
DEFAULT_BROADCAST = "255.255.255.255"
DEFAULT_PORT = 9

def load_hosts():
    with open("hosts.yaml", "r") as f:
        data = yaml.safe_load(f) or {}
    return data.get("hosts", {})

app = Flask(__name__)
app.secret_key = APP_SECRET

@app.route("/", methods=["GET"])
def index():
    hosts = load_hosts()
    return render_template("index.html", hosts=hosts)

@app.route("/wake/<key>", methods=["POST"])
def wake_saved(key):
    hosts = load_hosts()
    h = hosts.get(key)
    if not h:
        flash(f"Nieznany host: {key}")
        return redirect(url_for("index"))

    mac = h.get("mac", "").strip()
    bcast = (h.get("broadcast") or DEFAULT_BROADCAST).strip()
    port = int(h.get("port") or DEFAULT_PORT)
    interface = (h.get("interface") or "").strip() or None

    try:
        kwargs = {"ip_address": bcast, "port": port}
        if interface:
            kwargs["interface"] = interface
        send_magic_packet(mac, **kwargs)
        flash(f"Magic Packet wysłany do {h.get('name', key)} ({mac}) przez {bcast}:{port}" + (f" (iface {interface})" if interface else ""))
    except Exception as e:
        flash(f"Błąd WoL: {e}")
    return redirect(url_for("index"))

@app.route("/wake/manual", methods=["POST"])
def wake_manual():
    mac = request.form.get("mac", "").strip()
    bcast = (request.form.get("broadcast") or DEFAULT_BROADCAST).strip()
    port = int(request.form.get("port") or DEFAULT_PORT)
    interface = (request.form.get("interface") or "").strip() or None
    try:
        kwargs = {"ip_address": bcast, "port": port}
        if interface:
            kwargs["interface"] = interface
        send_magic_packet(mac, **kwargs)
        flash(f"Magic Packet wysłany do {mac} przez {bcast}:{port}" + (f" (iface {interface})" if interface else ""))
    except Exception as e:
        flash(f"Błąd WoL: {e}")
    return redirect(url_for("index"))
