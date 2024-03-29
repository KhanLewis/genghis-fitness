from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from products.models import Product


class BagView(View):
    def get(self, request):
        """ A view that renders the bag contents page """
        return render(request, 'bag/bag_detail.html')


class AddToBagView(View):
    def post(self, request, item_id):
        """ Add a quantity of the specified product to the shopping bag """
        product = get_object_or_404(Product, pk=item_id)
        quantity = int(request.POST.get('quantity'))
        redirect_url = request.POST.get('redirect_url')
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            if item_id in bag:
                if isinstance(bag.get(item_id), dict) and \
                        'items_by_size' in bag[item_id]:
                    if size in bag[item_id]['items_by_size']:
                        bag[item_id]['items_by_size'][size] += quantity
                        messages.success(request, f'Updated size \
                            {size.upper()} {product.name} quantity to \
                                {bag[item_id]["items_by_size"][size]}')
                    else:
                        bag[item_id]['items_by_size'][size] = quantity
                        messages.success(request, f'Added size {size.upper()} \
                            {product.name} to your bag')
                else:
                    bag[item_id] = {'items_by_size': {size: quantity}}
                    messages.success(request, f'Added size {size.upper()} \
                        {product.name} to your bag')
            else:
                bag[item_id] = {'items_by_size': {size: quantity}}
                messages.success(request, f'Added size {size.upper()} \
                    {product.name} to your bag')
        else:
            if item_id in bag:
                if isinstance(bag[item_id], int):
                    bag[item_id] += quantity
                    messages.success(request, f'Updated {product.name} \
                        quantity to {bag[item_id]}')
                else:
                    messages.error(request, f'Error: Invalid bag item format')
            else:
                bag[item_id] = quantity
                messages.success(request, f'Added {product.name} to your bag')

        request.session['bag'] = bag
        return redirect(redirect_url)


class AdjustBagView(View):
    def post(self, request, item_id):
        """Adjust the quantity of the specified product to the specified \
            amount"""
        product = get_object_or_404(Product, pk=item_id)
        quantity = int(request.POST.get('quantity'))
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            if quantity > 0:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Updated size {size.upper()}\
                     {product.name} quantity to \
                        {bag[item_id]["items_by_size"][size]}')
            else:
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)
                messages.success(request, f'Removed size \
                    {size.upper()} {product.name} from your bag')
        else:
            if quantity > 0:
                bag[item_id] = quantity
                messages.success(request, f'Updated \
                    {product.name} quantity to {bag[item_id]}')
            else:
                bag.pop(item_id)
                messages.success(request, f'Removed \
                    {product.name} from your bag')

        request.session['bag'] = bag
        return redirect(reverse('bag:view_bag'))


class RemoveFromBagView(View):
    def post(self, request, item_id):
        """Remove the item from the shopping bag"""
        try:
            product = get_object_or_404(Product, pk=item_id)
            size = None
            if 'product_size' in request.POST:
                size = request.POST['product_size']
            bag = request.session.get('bag', {})

            if size:
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} \
                    {product.name} from your bag')
            else:
                bag.pop(item_id)
                messages.success(request, f'Removed \
                    {product.name} from your bag')

            request.session['bag'] = bag
            return HttpResponse(status=200)
        except Exception as e:
            messages.error(request, f'Error removing item: {e}')
            return HttpResponse(status=500)
