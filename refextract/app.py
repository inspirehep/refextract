import logging

from flask import Flask, jsonify, make_response
from prometheus_flask_exporter.multiprocess import \
    GunicornInternalPrometheusMetrics
from webargs import fields
from webargs.flaskparser import FlaskParser

from refextract.references.api import (extract_journal_reference,
                                       extract_references_from_string,
                                       extract_references_from_url)

parser = FlaskParser()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.cfg", silent=True)

    @app.route("/extract_journal_info", methods=["POST"])
    @parser.use_args(
        {
            "publication_infos": fields.List(fields.Dict, required=True),
            "journal_kb_data": fields.Dict(required=True),
        },
        locations=("json",),
    )
    def extract_journal_info(args):
        publication_infos = args.pop("publication_infos")
        journal_kb_data = args.pop("journal_kb_data")
        extracted_publication_infos = []
        journal_dict = {"journals": journal_kb_data}
        try:
            for publication_info in publication_infos:
                if not publication_info.get('pubinfo_freetext'):
                    extracted_publication_infos.append({})
                    continue
                extracted_publication_info = extract_journal_reference(
                    publication_info["pubinfo_freetext"],
                    override_kbs_files=journal_dict,
                )
                if not extracted_publication_info:
                    extracted_publication_info = {}
                extracted_publication_infos.append(extracted_publication_info)
        except Exception as e:
            return make_response(
                jsonify(
                    {
                        "message": f"Can not extract publication info data. Reason: {str(e)}"
                    }
                ),
                500,
            )
        return jsonify({"extracted_publication_infos": extracted_publication_infos})

    @app.route("/extract_references_from_text", methods=["POST"])
    @parser.use_args(
        {
            "text": fields.String(required=True),
            "journal_kb_data": fields.Dict(required=True),
        },
        locations=("json",),
    )
    def extract_references_from_text(args):
        text = args.pop("text")
        journal_kb_data = args.pop("journal_kb_data")
        journal_dict = {"journals": journal_kb_data}
        try:
            extracted_references = extract_references_from_string(
                text,
                override_kbs_files=journal_dict,
                reference_format="{title},{volume},{page}",
            )
        except Exception as e:
            return make_response(
                jsonify({"message": f"Can not extract references. Reason: {str(e)}"}),
                500,
            )
        return jsonify({"extracted_references": extracted_references})

    @app.route("/extract_references_from_url", methods=["POST"])
    @parser.use_args(
        {
            "url": fields.String(required=True),
            "journal_kb_data": fields.Dict(required=True),
        },
        locations=("json",),
    )
    def extract_references_from_file_url(args):
        url = args.pop("url")
        journal_kb_data = args.pop("journal_kb_data")
        journal_dict = {"journals": journal_kb_data}
        try:
            extracted_references = extract_references_from_url(
                url,
                **{
                    "override_kbs_files": journal_dict,
                    "reference_format": "{title},{volume},{page}",
                },
            )
        except Exception as e:
            return make_response(
                jsonify({"message": f"Can not extract references. Reason: {str(e)}"}),
                500,
            )
        return jsonify({"extracted_references": extracted_references})

    return app


app = create_app()

if app.config.get('PROMETHEUS_ENABLE_EXPORTER_FLASK'):
    logging.info("Starting prometheus metrics exporter")
    metrics = GunicornInternalPrometheusMetrics.for_app_factory()
    metrics.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
