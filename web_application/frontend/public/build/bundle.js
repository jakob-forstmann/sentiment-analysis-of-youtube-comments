
(function(l, r) { if (!l || l.getElementById('livereloadscript')) return; r = l.createElement('script'); r.async = 1; r.src = '//' + (self.location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1'; r.id = 'livereloadscript'; l.getElementsByTagName('head')[0].appendChild(r) })(self.document);
var app = (function () {
    'use strict';

    function noop() { }
    function add_location(element, file, line, column, char) {
        element.__svelte_meta = {
            loc: { file, line, column, char }
        };
    }
    function run(fn) {
        return fn();
    }
    function blank_object() {
        return Object.create(null);
    }
    function run_all(fns) {
        fns.forEach(run);
    }
    function is_function(thing) {
        return typeof thing === 'function';
    }
    function safe_not_equal(a, b) {
        return a != a ? b == b : a !== b || ((a && typeof a === 'object') || typeof a === 'function');
    }
    function is_empty(obj) {
        return Object.keys(obj).length === 0;
    }
    function append(target, node) {
        target.appendChild(node);
    }
    function insert(target, node, anchor) {
        target.insertBefore(node, anchor || null);
    }
    function detach(node) {
        if (node.parentNode) {
            node.parentNode.removeChild(node);
        }
    }
    function element(name) {
        return document.createElement(name);
    }
    function text(data) {
        return document.createTextNode(data);
    }
    function space() {
        return text(' ');
    }
    function listen(node, event, handler, options) {
        node.addEventListener(event, handler, options);
        return () => node.removeEventListener(event, handler, options);
    }
    function attr(node, attribute, value) {
        if (value == null)
            node.removeAttribute(attribute);
        else if (node.getAttribute(attribute) !== value)
            node.setAttribute(attribute, value);
    }
    function children(element) {
        return Array.from(element.childNodes);
    }
    function set_input_value(input, value) {
        input.value = value == null ? '' : value;
    }
    function custom_event(type, detail, { bubbles = false, cancelable = false } = {}) {
        const e = document.createEvent('CustomEvent');
        e.initCustomEvent(type, bubbles, cancelable, detail);
        return e;
    }

    let current_component;
    function set_current_component(component) {
        current_component = component;
    }

    const dirty_components = [];
    const binding_callbacks = [];
    const render_callbacks = [];
    const flush_callbacks = [];
    const resolved_promise = Promise.resolve();
    let update_scheduled = false;
    function schedule_update() {
        if (!update_scheduled) {
            update_scheduled = true;
            resolved_promise.then(flush);
        }
    }
    function add_render_callback(fn) {
        render_callbacks.push(fn);
    }
    // flush() calls callbacks in this order:
    // 1. All beforeUpdate callbacks, in order: parents before children
    // 2. All bind:this callbacks, in reverse order: children before parents.
    // 3. All afterUpdate callbacks, in order: parents before children. EXCEPT
    //    for afterUpdates called during the initial onMount, which are called in
    //    reverse order: children before parents.
    // Since callbacks might update component values, which could trigger another
    // call to flush(), the following steps guard against this:
    // 1. During beforeUpdate, any updated components will be added to the
    //    dirty_components array and will cause a reentrant call to flush(). Because
    //    the flush index is kept outside the function, the reentrant call will pick
    //    up where the earlier call left off and go through all dirty components. The
    //    current_component value is saved and restored so that the reentrant call will
    //    not interfere with the "parent" flush() call.
    // 2. bind:this callbacks cannot trigger new flush() calls.
    // 3. During afterUpdate, any updated components will NOT have their afterUpdate
    //    callback called a second time; the seen_callbacks set, outside the flush()
    //    function, guarantees this behavior.
    const seen_callbacks = new Set();
    let flushidx = 0; // Do *not* move this inside the flush() function
    function flush() {
        const saved_component = current_component;
        do {
            // first, call beforeUpdate functions
            // and update components
            while (flushidx < dirty_components.length) {
                const component = dirty_components[flushidx];
                flushidx++;
                set_current_component(component);
                update(component.$$);
            }
            set_current_component(null);
            dirty_components.length = 0;
            flushidx = 0;
            while (binding_callbacks.length)
                binding_callbacks.pop()();
            // then, once components are updated, call
            // afterUpdate functions. This may cause
            // subsequent updates...
            for (let i = 0; i < render_callbacks.length; i += 1) {
                const callback = render_callbacks[i];
                if (!seen_callbacks.has(callback)) {
                    // ...so guard against infinite loops
                    seen_callbacks.add(callback);
                    callback();
                }
            }
            render_callbacks.length = 0;
        } while (dirty_components.length);
        while (flush_callbacks.length) {
            flush_callbacks.pop()();
        }
        update_scheduled = false;
        seen_callbacks.clear();
        set_current_component(saved_component);
    }
    function update($$) {
        if ($$.fragment !== null) {
            $$.update();
            run_all($$.before_update);
            const dirty = $$.dirty;
            $$.dirty = [-1];
            $$.fragment && $$.fragment.p($$.ctx, dirty);
            $$.after_update.forEach(add_render_callback);
        }
    }
    const outroing = new Set();
    let outros;
    function transition_in(block, local) {
        if (block && block.i) {
            outroing.delete(block);
            block.i(local);
        }
    }
    function transition_out(block, local, detach, callback) {
        if (block && block.o) {
            if (outroing.has(block))
                return;
            outroing.add(block);
            outros.c.push(() => {
                outroing.delete(block);
                if (callback) {
                    if (detach)
                        block.d(1);
                    callback();
                }
            });
            block.o(local);
        }
        else if (callback) {
            callback();
        }
    }
    function create_component(block) {
        block && block.c();
    }
    function mount_component(component, target, anchor, customElement) {
        const { fragment, after_update } = component.$$;
        fragment && fragment.m(target, anchor);
        if (!customElement) {
            // onMount happens before the initial afterUpdate
            add_render_callback(() => {
                const new_on_destroy = component.$$.on_mount.map(run).filter(is_function);
                // if the component was destroyed immediately
                // it will update the `$$.on_destroy` reference to `null`.
                // the destructured on_destroy may still reference to the old array
                if (component.$$.on_destroy) {
                    component.$$.on_destroy.push(...new_on_destroy);
                }
                else {
                    // Edge case - component was destroyed immediately,
                    // most likely as a result of a binding initialising
                    run_all(new_on_destroy);
                }
                component.$$.on_mount = [];
            });
        }
        after_update.forEach(add_render_callback);
    }
    function destroy_component(component, detaching) {
        const $$ = component.$$;
        if ($$.fragment !== null) {
            run_all($$.on_destroy);
            $$.fragment && $$.fragment.d(detaching);
            // TODO null out other refs, including component.$$ (but need to
            // preserve final state?)
            $$.on_destroy = $$.fragment = null;
            $$.ctx = [];
        }
    }
    function make_dirty(component, i) {
        if (component.$$.dirty[0] === -1) {
            dirty_components.push(component);
            schedule_update();
            component.$$.dirty.fill(0);
        }
        component.$$.dirty[(i / 31) | 0] |= (1 << (i % 31));
    }
    function init(component, options, instance, create_fragment, not_equal, props, append_styles, dirty = [-1]) {
        const parent_component = current_component;
        set_current_component(component);
        const $$ = component.$$ = {
            fragment: null,
            ctx: [],
            // state
            props,
            update: noop,
            not_equal,
            bound: blank_object(),
            // lifecycle
            on_mount: [],
            on_destroy: [],
            on_disconnect: [],
            before_update: [],
            after_update: [],
            context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
            // everything else
            callbacks: blank_object(),
            dirty,
            skip_bound: false,
            root: options.target || parent_component.$$.root
        };
        append_styles && append_styles($$.root);
        let ready = false;
        $$.ctx = instance
            ? instance(component, options.props || {}, (i, ret, ...rest) => {
                const value = rest.length ? rest[0] : ret;
                if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
                    if (!$$.skip_bound && $$.bound[i])
                        $$.bound[i](value);
                    if (ready)
                        make_dirty(component, i);
                }
                return ret;
            })
            : [];
        $$.update();
        ready = true;
        run_all($$.before_update);
        // `false` as a special case of no DOM component
        $$.fragment = create_fragment ? create_fragment($$.ctx) : false;
        if (options.target) {
            if (options.hydrate) {
                const nodes = children(options.target);
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                $$.fragment && $$.fragment.l(nodes);
                nodes.forEach(detach);
            }
            else {
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                $$.fragment && $$.fragment.c();
            }
            if (options.intro)
                transition_in(component.$$.fragment);
            mount_component(component, options.target, options.anchor, options.customElement);
            flush();
        }
        set_current_component(parent_component);
    }
    /**
     * Base class for Svelte components. Used when dev=false.
     */
    class SvelteComponent {
        $destroy() {
            destroy_component(this, 1);
            this.$destroy = noop;
        }
        $on(type, callback) {
            if (!is_function(callback)) {
                return noop;
            }
            const callbacks = (this.$$.callbacks[type] || (this.$$.callbacks[type] = []));
            callbacks.push(callback);
            return () => {
                const index = callbacks.indexOf(callback);
                if (index !== -1)
                    callbacks.splice(index, 1);
            };
        }
        $set($$props) {
            if (this.$$set && !is_empty($$props)) {
                this.$$.skip_bound = true;
                this.$$set($$props);
                this.$$.skip_bound = false;
            }
        }
    }

    function dispatch_dev(type, detail) {
        document.dispatchEvent(custom_event(type, Object.assign({ version: '3.55.0' }, detail), { bubbles: true }));
    }
    function append_dev(target, node) {
        dispatch_dev('SvelteDOMInsert', { target, node });
        append(target, node);
    }
    function insert_dev(target, node, anchor) {
        dispatch_dev('SvelteDOMInsert', { target, node, anchor });
        insert(target, node, anchor);
    }
    function detach_dev(node) {
        dispatch_dev('SvelteDOMRemove', { node });
        detach(node);
    }
    function listen_dev(node, event, handler, options, has_prevent_default, has_stop_propagation) {
        const modifiers = options === true ? ['capture'] : options ? Array.from(Object.keys(options)) : [];
        if (has_prevent_default)
            modifiers.push('preventDefault');
        if (has_stop_propagation)
            modifiers.push('stopPropagation');
        dispatch_dev('SvelteDOMAddEventListener', { node, event, handler, modifiers });
        const dispose = listen(node, event, handler, options);
        return () => {
            dispatch_dev('SvelteDOMRemoveEventListener', { node, event, handler, modifiers });
            dispose();
        };
    }
    function attr_dev(node, attribute, value) {
        attr(node, attribute, value);
        if (value == null)
            dispatch_dev('SvelteDOMRemoveAttribute', { node, attribute });
        else
            dispatch_dev('SvelteDOMSetAttribute', { node, attribute, value });
    }
    function set_data_dev(text, data) {
        data = '' + data;
        if (text.wholeText === data)
            return;
        dispatch_dev('SvelteDOMSetData', { node: text, data });
        text.data = data;
    }
    function validate_slots(name, slot, keys) {
        for (const slot_key of Object.keys(slot)) {
            if (!~keys.indexOf(slot_key)) {
                console.warn(`<${name}> received an unexpected slot "${slot_key}".`);
            }
        }
    }
    /**
     * Base class for Svelte components with some minor dev-enhancements. Used when dev=true.
     */
    class SvelteComponentDev extends SvelteComponent {
        constructor(options) {
            if (!options || (!options.target && !options.$$inline)) {
                throw new Error("'target' is a required option");
            }
            super();
        }
        $destroy() {
            super.$destroy();
            this.$destroy = () => {
                console.warn('Component was already destroyed'); // eslint-disable-line no-console
            };
        }
        $capture_state() { }
        $inject_state() { }
    }

    /* src\components\Navbar.svelte generated by Svelte v3.55.0 */

    const file$6 = "src\\components\\Navbar.svelte";

    function create_fragment$6(ctx) {
    	let navbar;
    	let div;
    	let h1;

    	const block = {
    		c: function create() {
    			navbar = element("navbar");
    			div = element("div");
    			h1 = element("h1");
    			h1.textContent = "YouTube Comments";
    			add_location(h1, file$6, 4, 20, 68);
    			attr_dev(div, "class", "logo");
    			add_location(div, file$6, 4, 2, 50);
    			attr_dev(navbar, "class", "navbar svelte-1u6yw98");
    			add_location(navbar, file$6, 3, 0, 23);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, navbar, anchor);
    			append_dev(navbar, div);
    			append_dev(div, h1);
    		},
    		p: noop,
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(navbar);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$6.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$6($$self, $$props) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('Navbar', slots, []);
    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Navbar> was created with unknown prop '${key}'`);
    	});

    	return [];
    }

    class Navbar extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$6, create_fragment$6, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "Navbar",
    			options,
    			id: create_fragment$6.name
    		});
    	}
    }

    /* src\components\Searchbar.svelte generated by Svelte v3.55.0 */

    const file$5 = "src\\components\\Searchbar.svelte";

    function create_fragment$5(ctx) {
    	let t0;
    	let t1;
    	let div1;
    	let div0;
    	let label;
    	let t3;
    	let input;
    	let t4;
    	let button;
    	let mounted;
    	let dispose;

    	const block = {
    		c: function create() {
    			t0 = text(/*searchUrl*/ ctx[0]);
    			t1 = space();
    			div1 = element("div");
    			div0 = element("div");
    			label = element("label");
    			label.textContent = "Enter YouTube video link to get Comments";
    			t3 = space();
    			input = element("input");
    			t4 = space();
    			button = element("button");
    			button.textContent = "Go";
    			attr_dev(label, "for", "search-bar");
    			attr_dev(label, "class", "search-label");
    			add_location(label, file$5, 9, 4, 166);
    			attr_dev(input, "type", "text");
    			attr_dev(input, "id", "search-bar");
    			attr_dev(input, "class", "search-bar");
    			add_location(input, file$5, 12, 4, 279);
    			attr_dev(div0, "class", "search-area svelte-1n8ul57");
    			add_location(div0, file$5, 8, 2, 135);
    			attr_dev(button, "class", "search-submit");
    			add_location(button, file$5, 19, 2, 405);
    			attr_dev(div1, "class", "main-search-area svelte-1n8ul57");
    			add_location(div1, file$5, 7, 0, 101);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, t0, anchor);
    			insert_dev(target, t1, anchor);
    			insert_dev(target, div1, anchor);
    			append_dev(div1, div0);
    			append_dev(div0, label);
    			append_dev(div0, t3);
    			append_dev(div0, input);
    			set_input_value(input, /*searchUrl*/ ctx[0]);
    			append_dev(div1, t4);
    			append_dev(div1, button);

    			if (!mounted) {
    				dispose = [
    					listen_dev(input, "input", /*input_input_handler*/ ctx[1]),
    					listen_dev(button, "click", searchVideo, false, false, false)
    				];

    				mounted = true;
    			}
    		},
    		p: function update(ctx, [dirty]) {
    			if (dirty & /*searchUrl*/ 1) set_data_dev(t0, /*searchUrl*/ ctx[0]);

    			if (dirty & /*searchUrl*/ 1 && input.value !== /*searchUrl*/ ctx[0]) {
    				set_input_value(input, /*searchUrl*/ ctx[0]);
    			}
    		},
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(t0);
    			if (detaching) detach_dev(t1);
    			if (detaching) detach_dev(div1);
    			mounted = false;
    			run_all(dispose);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$5.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    async function searchVideo(event) {
    	
    }

    function instance$5($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('Searchbar', slots, []);
    	let searchUrl = "";
    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Searchbar> was created with unknown prop '${key}'`);
    	});

    	function input_input_handler() {
    		searchUrl = this.value;
    		$$invalidate(0, searchUrl);
    	}

    	$$self.$capture_state = () => ({ searchUrl, searchVideo });

    	$$self.$inject_state = $$props => {
    		if ('searchUrl' in $$props) $$invalidate(0, searchUrl = $$props.searchUrl);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	return [searchUrl, input_input_handler];
    }

    class Searchbar extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$5, create_fragment$5, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "Searchbar",
    			options,
    			id: create_fragment$5.name
    		});
    	}
    }

    /* src\components\VideoCard.svelte generated by Svelte v3.55.0 */

    const file$4 = "src\\components\\VideoCard.svelte";

    function create_fragment$4(ctx) {
    	let div3;
    	let div1;
    	let div0;
    	let span0;
    	let t1;
    	let span1;
    	let t3;
    	let span2;
    	let t5;
    	let div2;
    	let h1;
    	let t7;
    	let p;

    	const block = {
    		c: function create() {
    			div3 = element("div");
    			div1 = element("div");
    			div0 = element("div");
    			span0 = element("span");
    			span0.textContent = "5 Likes";
    			t1 = space();
    			span1 = element("span");
    			span1.textContent = "10 Comments";
    			t3 = space();
    			span2 = element("span");
    			span2.textContent = "100 Views";
    			t5 = space();
    			div2 = element("div");
    			h1 = element("h1");
    			h1.textContent = "Title of the Video";
    			t7 = space();
    			p = element("p");
    			p.textContent = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptates\r\n      eligendi velit, doloribus ut ducimus laborum, et vitae iusto nobis omnis a\r\n      impedit repudiandae laudantium voluptate vero eos nostrum quas illum? Ipsa\r\n      deleniti totam dolor vel, laboriosam ex natus! Odit inventore mollitia\r\n      corporis doloribus quaerat, vel totam illum labore repellendus similique\r\n      porro perferendis non dolores! Exercitationem dolorem facilis quis officia\r\n      facere?";
    			attr_dev(span0, "class", "no-likes svelte-13iarxb");
    			add_location(span0, file$4, 6, 6, 116);
    			attr_dev(span1, "class", "no-comments svelte-13iarxb");
    			add_location(span1, file$4, 7, 6, 161);
    			attr_dev(span2, "class", "no-views svelte-13iarxb");
    			add_location(span2, file$4, 8, 6, 213);
    			attr_dev(div0, "class", "card-thumbnail svelte-13iarxb");
    			add_location(div0, file$4, 5, 4, 80);
    			attr_dev(div1, "class", "card-left svelte-13iarxb");
    			add_location(div1, file$4, 4, 2, 51);
    			attr_dev(h1, "class", "card-title svelte-13iarxb");
    			add_location(h1, file$4, 12, 4, 308);
    			attr_dev(p, "class", "card-description svelte-13iarxb");
    			add_location(p, file$4, 13, 4, 360);
    			attr_dev(div2, "class", "card-right svelte-13iarxb");
    			add_location(div2, file$4, 11, 2, 278);
    			attr_dev(div3, "class", "video-card svelte-13iarxb");
    			add_location(div3, file$4, 3, 0, 23);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div3, anchor);
    			append_dev(div3, div1);
    			append_dev(div1, div0);
    			append_dev(div0, span0);
    			append_dev(div0, t1);
    			append_dev(div0, span1);
    			append_dev(div0, t3);
    			append_dev(div0, span2);
    			append_dev(div3, t5);
    			append_dev(div3, div2);
    			append_dev(div2, h1);
    			append_dev(div2, t7);
    			append_dev(div2, p);
    		},
    		p: noop,
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div3);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$4.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$4($$self, $$props) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('VideoCard', slots, []);
    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<VideoCard> was created with unknown prop '${key}'`);
    	});

    	return [];
    }

    class VideoCard extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$4, create_fragment$4, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "VideoCard",
    			options,
    			id: create_fragment$4.name
    		});
    	}
    }

    /* src\components\CommentsCard.svelte generated by Svelte v3.55.0 */

    const file$3 = "src\\components\\CommentsCard.svelte";

    function create_fragment$3(ctx) {
    	let div2;
    	let div0;
    	let h3;
    	let t1;
    	let h6;
    	let t3;
    	let div1;
    	let ol;
    	let li0;
    	let t5;
    	let li1;
    	let t7;
    	let li2;

    	const block = {
    		c: function create() {
    			div2 = element("div");
    			div0 = element("div");
    			h3 = element("h3");
    			h3.textContent = "Negative";
    			t1 = space();
    			h6 = element("h6");
    			h6.textContent = "30%";
    			t3 = space();
    			div1 = element("div");
    			ol = element("ol");
    			li0 = element("li");
    			li0.textContent = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Recusandae\r\n        fugiat perspiciatis sit at veritatis ipsum illo quibusdam incidunt dicta\r\n        harum architecto, ipsam aperiam tenetur blanditiis quaerat ipsa iste\r\n        inventore eligendi?";
    			t5 = space();
    			li1 = element("li");
    			li1.textContent = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Recusandae\r\n        fugiat perspiciatis sit at veritatis ipsum illo quibusdam incidunt dicta\r\n        harum architecto, ipsam aperiam tenetur blanditiis quaerat ipsa iste\r\n        inventore eligendi?";
    			t7 = space();
    			li2 = element("li");
    			li2.textContent = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Recusandae\r\n        fugiat perspiciatis sit at veritatis ipsum illo quibusdam incidunt dicta\r\n        harum architecto, ipsam aperiam tenetur blanditiis quaerat ipsa iste\r\n        inventore eligendi?";
    			attr_dev(h3, "class", "head");
    			add_location(h3, file$3, 5, 4, 78);
    			attr_dev(h6, "class", "percentage");
    			add_location(h6, file$3, 6, 4, 114);
    			attr_dev(div0, "class", "analytics");
    			add_location(div0, file$3, 4, 2, 49);
    			attr_dev(li0, "class", "comment");
    			add_location(li0, file$3, 11, 6, 201);
    			attr_dev(li1, "class", "comment");
    			add_location(li1, file$3, 17, 6, 509);
    			attr_dev(li2, "class", "comment");
    			add_location(li2, file$3, 23, 6, 817);
    			attr_dev(ol, "class", "svelte-18h1a24");
    			add_location(ol, file$3, 10, 4, 189);
    			attr_dev(div1, "class", "comments svelte-18h1a24");
    			add_location(div1, file$3, 9, 2, 161);
    			attr_dev(div2, "class", "negative");
    			add_location(div2, file$3, 3, 0, 23);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div2, anchor);
    			append_dev(div2, div0);
    			append_dev(div0, h3);
    			append_dev(div0, t1);
    			append_dev(div0, h6);
    			append_dev(div2, t3);
    			append_dev(div2, div1);
    			append_dev(div1, ol);
    			append_dev(ol, li0);
    			append_dev(ol, t5);
    			append_dev(ol, li1);
    			append_dev(ol, t7);
    			append_dev(ol, li2);
    		},
    		p: noop,
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div2);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$3.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$3($$self, $$props) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('CommentsCard', slots, []);
    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<CommentsCard> was created with unknown prop '${key}'`);
    	});

    	return [];
    }

    class CommentsCard extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$3, create_fragment$3, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "CommentsCard",
    			options,
    			id: create_fragment$3.name
    		});
    	}
    }

    /* src\components\VideoComments.svelte generated by Svelte v3.55.0 */
    const file$2 = "src\\components\\VideoComments.svelte";

    function create_fragment$2(ctx) {
    	let div;
    	let commentscard0;
    	let t0;
    	let commentscard1;
    	let t1;
    	let commentscard2;
    	let current;

    	commentscard0 = new CommentsCard({
    			props: { head: "Negative" },
    			$$inline: true
    		});

    	commentscard1 = new CommentsCard({
    			props: { head: "Neutral" },
    			$$inline: true
    		});

    	commentscard2 = new CommentsCard({
    			props: { head: "Positive" },
    			$$inline: true
    		});

    	const block = {
    		c: function create() {
    			div = element("div");
    			create_component(commentscard0.$$.fragment);
    			t0 = space();
    			create_component(commentscard1.$$.fragment);
    			t1 = space();
    			create_component(commentscard2.$$.fragment);
    			attr_dev(div, "class", "classification svelte-1ae95gd");
    			add_location(div, file$2, 4, 0, 76);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div, anchor);
    			mount_component(commentscard0, div, null);
    			append_dev(div, t0);
    			mount_component(commentscard1, div, null);
    			append_dev(div, t1);
    			mount_component(commentscard2, div, null);
    			current = true;
    		},
    		p: noop,
    		i: function intro(local) {
    			if (current) return;
    			transition_in(commentscard0.$$.fragment, local);
    			transition_in(commentscard1.$$.fragment, local);
    			transition_in(commentscard2.$$.fragment, local);
    			current = true;
    		},
    		o: function outro(local) {
    			transition_out(commentscard0.$$.fragment, local);
    			transition_out(commentscard1.$$.fragment, local);
    			transition_out(commentscard2.$$.fragment, local);
    			current = false;
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div);
    			destroy_component(commentscard0);
    			destroy_component(commentscard1);
    			destroy_component(commentscard2);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$2.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$2($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('VideoComments', slots, []);
    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<VideoComments> was created with unknown prop '${key}'`);
    	});

    	$$self.$capture_state = () => ({ CommentsCard });
    	return [];
    }

    class VideoComments extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$2, create_fragment$2, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "VideoComments",
    			options,
    			id: create_fragment$2.name
    		});
    	}
    }

    /* src\components\Footer.svelte generated by Svelte v3.55.0 */

    const file$1 = "src\\components\\Footer.svelte";

    function create_fragment$1(ctx) {
    	let footer;
    	let h1;

    	const block = {
    		c: function create() {
    			footer = element("footer");
    			h1 = element("h1");
    			h1.textContent = "Footer";
    			add_location(h1, file$1, 3, 2, 33);
    			attr_dev(footer, "class", "svelte-2f2kbk");
    			add_location(footer, file$1, 2, 0, 21);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, footer, anchor);
    			append_dev(footer, h1);
    		},
    		p: noop,
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(footer);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$1.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$1($$self, $$props) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('Footer', slots, []);
    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Footer> was created with unknown prop '${key}'`);
    	});

    	return [];
    }

    class Footer extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$1, create_fragment$1, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "Footer",
    			options,
    			id: create_fragment$1.name
    		});
    	}
    }

    /* src\App.svelte generated by Svelte v3.55.0 */
    const file = "src\\App.svelte";

    function create_fragment(ctx) {
    	let navbar;
    	let t0;
    	let main;
    	let searchbar;
    	let t1;
    	let videocard;
    	let t2;
    	let videocomments;
    	let t3;
    	let footer;
    	let current;
    	navbar = new Navbar({ $$inline: true });
    	searchbar = new Searchbar({ $$inline: true });
    	videocard = new VideoCard({ $$inline: true });
    	videocomments = new VideoComments({ $$inline: true });
    	footer = new Footer({ $$inline: true });

    	const block = {
    		c: function create() {
    			create_component(navbar.$$.fragment);
    			t0 = space();
    			main = element("main");
    			create_component(searchbar.$$.fragment);
    			t1 = space();
    			create_component(videocard.$$.fragment);
    			t2 = space();
    			create_component(videocomments.$$.fragment);
    			t3 = space();
    			create_component(footer.$$.fragment);
    			attr_dev(main, "class", "svelte-6j4r2i");
    			add_location(main, file, 8, 0, 316);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			mount_component(navbar, target, anchor);
    			insert_dev(target, t0, anchor);
    			insert_dev(target, main, anchor);
    			mount_component(searchbar, main, null);
    			append_dev(main, t1);
    			mount_component(videocard, main, null);
    			append_dev(main, t2);
    			mount_component(videocomments, main, null);
    			insert_dev(target, t3, anchor);
    			mount_component(footer, target, anchor);
    			current = true;
    		},
    		p: noop,
    		i: function intro(local) {
    			if (current) return;
    			transition_in(navbar.$$.fragment, local);
    			transition_in(searchbar.$$.fragment, local);
    			transition_in(videocard.$$.fragment, local);
    			transition_in(videocomments.$$.fragment, local);
    			transition_in(footer.$$.fragment, local);
    			current = true;
    		},
    		o: function outro(local) {
    			transition_out(navbar.$$.fragment, local);
    			transition_out(searchbar.$$.fragment, local);
    			transition_out(videocard.$$.fragment, local);
    			transition_out(videocomments.$$.fragment, local);
    			transition_out(footer.$$.fragment, local);
    			current = false;
    		},
    		d: function destroy(detaching) {
    			destroy_component(navbar, detaching);
    			if (detaching) detach_dev(t0);
    			if (detaching) detach_dev(main);
    			destroy_component(searchbar);
    			destroy_component(videocard);
    			destroy_component(videocomments);
    			if (detaching) detach_dev(t3);
    			destroy_component(footer, detaching);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('App', slots, []);
    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<App> was created with unknown prop '${key}'`);
    	});

    	$$self.$capture_state = () => ({
    		Navbar,
    		Searchbar,
    		VideoCard,
    		VideoComments,
    		Footer
    	});

    	return [];
    }

    class App extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance, create_fragment, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "App",
    			options,
    			id: create_fragment.name
    		});
    	}
    }

    const app = new App({
        target: document.body,
        props: {
            name: 'world'
        }
    });

    return app;

})();
//# sourceMappingURL=bundle.js.map
